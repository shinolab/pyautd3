use anyhow::Result;
use convert_case::{Case, Casing};

use std::{
    collections::HashSet,
    fs::File,
    io::{BufWriter, Write},
    path::Path,
};

use itertools::Itertools;

use crate::{
    parse::{Arg, Const, Enum, Function, Struct},
    types::{InOut, Type},
    Union,
};

pub struct PythonGenerator {
    functions: Vec<Function>,
    constants: Vec<Const>,
    enums: Vec<Enum>,
    unions: Vec<Union>,
    structs: Vec<Struct>,
}

impl PythonGenerator {
    fn sub_reserve(str: &str) -> String {
        match str {
            "lambda" => "lambda_".to_string(),
            "None" => "None_".to_string(),
            _ => str.to_owned(),
        }
    }

    fn to_python_func_name(name: &str) -> String {
        let name = name[4..].to_string();
        name.to_case(Case::Snake)
    }

    fn to_return_ty(ty: &Type) -> String {
        match ty {
            Type::Int8 => "ctypes.c_int8".to_string(),
            Type::Int16 => "ctypes.c_int16".to_string(),
            Type::Int32 => "ctypes.c_int32".to_string(),
            Type::Int64 => "ctypes.c_int64".to_string(),
            Type::UInt8 => "ctypes.c_uint8".to_string(),
            Type::UInt16 => "ctypes.c_uint16".to_string(),
            Type::UInt32 => "ctypes.c_uint32".to_string(),
            Type::UInt64 => "ctypes.c_uint64".to_string(),
            Type::Void => "None".to_string(),
            Type::Char => "ctypes.c_char".to_string(),
            Type::Float32 => "ctypes.c_float".to_string(),
            Type::Float64 => "ctypes.c_float".to_string(),
            Type::Bool => "ctypes.c_bool".to_string(),
            Type::VoidPtr => "ctypes.c_void_p".to_string(),
            Type::Custom(ref s) => match s.as_str() {
                "* mut c_char" => "ctypes.c_char_p".to_string(),
                "[u8 ; 2]" => "ctypes.c_uint8 * 2".to_string(),
                s if s.ends_with("Tag") => "ctypes.c_uint8".to_string(),
                s => s.to_owned(),
            },
        }
    }

    fn to_python_ty(ty: &Type) -> String {
        match ty {
            Type::Int8 => "int".to_string(),
            Type::Int16 => "int".to_string(),
            Type::Int32 => "int".to_string(),
            Type::Int64 => "int".to_string(),
            Type::UInt8 => "int".to_string(),
            Type::UInt16 => "int".to_string(),
            Type::UInt32 => "int".to_string(),
            Type::UInt64 => "int".to_string(),
            Type::Float32 => "float".to_string(),
            Type::Float64 => "float".to_string(),
            Type::Bool => "bool".to_string(),
            Type::Custom(ref s) => format!("\"{}\"", s),
            Type::VoidPtr => "ctypes.c_void_p".to_string(),
            t => unimplemented!("{:?}", t),
        }
    }

    fn to_arg(arg: &Arg) -> String {
        match arg.pointer {
            0 => match arg.ty {
                Type::Int8 => "ctypes.c_int8".to_owned(),
                Type::Int16 => "ctypes.c_int16".to_owned(),
                Type::Int32 => "ctypes.c_int32".to_owned(),
                Type::Int64 => "ctypes.c_int64".to_owned(),
                Type::UInt8 => "ctypes.c_uint8".to_owned(),
                Type::UInt16 => "ctypes.c_uint16".to_owned(),
                Type::UInt32 => "ctypes.c_uint32".to_owned(),
                Type::UInt64 => "ctypes.c_uint64".to_owned(),
                Type::Void => panic!("void is not supported in argument"),
                Type::Char => "ctypes.c_char".to_owned(),
                Type::Float32 => "ctypes.c_float".to_owned(),
                Type::Float64 => "ctypes.c_float".to_owned(),
                Type::Bool => "ctypes.c_bool".to_owned(),
                Type::VoidPtr => "ctypes.c_void_p".to_owned(),
                Type::Custom(ref s) => s.to_owned(),
            },
            1 => match arg.ty {
                Type::Int8 => "ctypes.POINTER(ctypes.c_int8)".to_owned(),
                Type::Int16 => "ctypes.POINTER(ctypes.c_int16)".to_owned(),
                Type::Int32 => "ctypes.POINTER(ctypes.c_int32)".to_owned(),
                Type::Int64 => "ctypes.POINTER(ctypes.c_int64)".to_owned(),
                Type::UInt8 => "ctypes.POINTER(ctypes.c_uint8)".to_owned(),
                Type::UInt16 => "ctypes.POINTER(ctypes.c_uint16)".to_owned(),
                Type::UInt32 => "ctypes.POINTER(ctypes.c_uint32)".to_owned(),
                Type::UInt64 => "ctypes.POINTER(ctypes.c_uint64)".to_owned(),
                Type::Void => unimplemented!(),
                Type::Char => "ctypes.c_char_p".to_owned(),
                Type::Float32 => "ctypes.POINTER(ctypes.c_float)".to_owned(),
                Type::Float64 => "ctypes.POINTER(ctypes.c_float)".to_owned(),
                Type::Bool => "ctypes.POINTER(ctypes.c_bool)".to_owned(),
                Type::VoidPtr => "ctypes.POINTER(ctypes.c_void_p)".to_owned(),
                Type::Custom(ref s) => format!("ctypes.POINTER({})", s),
            },
            2 => match arg.ty {
                Type::Int32 => "ctypes.POINTER(ctypes.POINTER(ctypes.c_int32))".to_owned(),
                Type::Float32 => "ctypes.POINTER(ctypes.POINTER(ctypes.c_float))".to_owned(),
                Type::Float64 => "ctypes.POINTER(ctypes.POINTER(ctypes.c_float))".to_owned(),
                Type::Custom(ref s) => format!("ctypes.POINTER(ctypes.POINTER({}))", s),
                _ => unimplemented!(),
            },
            _ => {
                panic!("truple or more pointer is not supported")
            }
        }
    }

    fn to_python_arg(arg: &Arg) -> &str {
        match arg.pointer {
            0 => match arg.ty {
                Type::Int8 => "int",
                Type::Int16 => "int",
                Type::Int32 => "int",
                Type::Int64 => "int",
                Type::UInt8 => "int",
                Type::UInt16 => "int",
                Type::UInt32 => "int",
                Type::UInt64 => "int",
                Type::Void => panic!("void is not supported in argument"),
                Type::Char => panic!("void is not supported in argument"),
                Type::Float32 => "float",
                Type::Float64 => "float",
                Type::Bool => "bool",
                Type::VoidPtr => "ctypes.c_void_p | None",
                Type::Custom(ref s) => s,
            },
            1 => match arg.ty {
                Type::Int8 => "ctypes.Array[ctypes.c_int8] | None",
                Type::Int16 => "ctypes.Array[ctypes.c_int16] | None",
                Type::Int32 => "ctypes.Array[ctypes.c_int32] | None",
                Type::Int64 => "ctypes.Array[ctypes.c_int64] | None",
                Type::UInt8 => "ctypes.Array[ctypes.c_uint8] | None",
                Type::UInt16 => "ctypes.Array[ctypes.c_uint16] | None",
                Type::UInt32 => "ctypes.Array[ctypes.c_uint32] | None",
                Type::UInt64 => "ctypes.Array[ctypes.c_uint64] | None",
                Type::Void => unimplemented!(),
                Type::Char => match arg.inout {
                    InOut::In => "bytes",
                    InOut::Out => "ctypes.Array[ctypes.c_char] | None",
                    _ => "Any",
                },
                Type::Float32 => "ctypes.Array[ctypes.c_float] | None",
                Type::Float64 => "ctypes.Array[ctypes.c_float] | None",
                Type::Bool => "ctypes.Array[ctypes.c_bool] | None",
                Type::VoidPtr => "ctypes.Array[ctypes.c_void_p] | None",
                Type::Custom(_) => "ctypes.Array | None",
            },
            2 => match arg.ty {
                Type::Int32 => "ctypes.Array[ctypes.Array[ctypes.c_int32]]",
                Type::Custom(_) => "ctypes.Array",
                _ => "Any",
            },
            _ => {
                panic!("triple or more pointer is not supported")
            }
        }
    }

    fn get_filename(name: &str) -> String {
        format!("{}.py", name.replace('-', "_"))
    }
}

impl PythonGenerator {
    pub fn register_const(mut self, constants: Vec<Const>) -> Self {
        self.constants.extend(constants);
        self
    }

    pub fn register_enum(mut self, enums: Vec<Enum>) -> Self {
        self.enums.extend(enums);
        self
    }

    pub fn register_union(mut self, unions: Vec<Union>) -> Self {
        self.unions.extend(unions);
        self
    }

    pub fn register_func(mut self, functions: Vec<Function>) -> Self {
        self.functions.extend(functions);
        self
    }

    pub fn register_struct(mut self, e: Vec<crate::parse::Struct>) -> Self {
        self.structs.extend(e.into_iter().filter(|s| {
            !matches!(
                s.name.as_str(),
                "CustomGain"
                    | "CustomModulation"
                    | "DynamicDatagramPack"
                    | "DynamicDatagramPack2"
                    | "DynamicLinkBuilder"
                    | "DynamicForceFan"
                    | "DynamicForceFanOp"
                    | "DynamicReadsFPGAState"
                    | "DynamicReadsFPGAStateOp"
                    | "SyncGroupGuard"
                    | "SyncController"
                    | "SyncControllerBuilder"
                    | "SyncLink"
                    | "SyncLinkBuilder"
                    | "DynamicDatagramWithSegment"
                    | "DynamicDatagramWithSegmentTransition"
                    | "DynamicPhaseFilter"
                    | "DynamicPhaseFilterOp"
                    | "DynamicDebugSettings"
                    | "DynamicDebugSettingOp"
                    | "DebugSettings"
                    | "RawGain"
                    | "RawModulation"
                    | "DynamicDatagramTuple"
                    | "DynamicOperationGeneratorTuple"
                    | "DynamicDatagramWithParallelThreshold"
                    | "DynamicDatagramWithTimeout"
                    | "DynamicOperationGenerator"
                    | "DynamicOperationGeneratorPack"
                    | "ControllerWrap"
            )
        }));
        self
    }

    pub fn new() -> Self {
        Self {
            functions: Vec::new(),
            constants: Vec::new(),
            enums: Vec::new(),
            unions: Vec::new(),
            structs: Vec::new(),
        }
    }

    pub fn write<P: AsRef<Path>>(self, path: P, crate_name: &str) -> Result<()> {
        let mut w = BufWriter::new(File::create(
            path.as_ref().join(Self::get_filename(crate_name)),
        )?);

        writeln!(
            w,
            r"# This file is autogenerated
import threading
import ctypes
import os
from pyautd3.native_methods.structs import Vector3, Quaternion, FfiFuture, LocalFfiFuture, SamplingConfig"
        )?;

        let owns = |ty: &Type| {
            if let Type::Custom(ref s) = ty {
                if self.enums.iter().any(|e| &e.name == s)
                    || self.structs.iter().any(|e| &e.name == s)
                {
                    return None;
                }
                Some(s.to_string())
            } else {
                None
            }
        };
        let used_ty: HashSet<_> = self
            .functions
            .iter()
            .flat_map(|f| {
                f.args
                    .iter()
                    .filter_map(|arg| owns(&arg.ty))
                    .chain([&f.return_ty].iter().filter_map(|&ty| owns(ty)))
                    .collect::<Vec<_>>()
            })
            .collect();

        let def_ty = vec![
            "SyncMode",
            "GPIOIn",
            "RuntimePtr",
            "GainPtr",
            "ModulationPtr",
            "LinkPtr",
            "ControllerPtr",
            "LinkBuilderPtr",
            "CachePtr",
            "ResultI32",
            "ResultU64",
            "GroupKVMapPtr",
            "ResultDatagram",
            "ResultModulationCalc",
            "ModulationCalcPtr",
            "TransducerPtr",
            "GeometryPtr",
            "DatagramSpecialPtr",
            "DatagramPtr",
            "ResultModulation",
            "FirmwareInfoListPtr",
            "ResultController",
            "DevicePtr",
            "GainCalcDrivesMapPtr",
            "ResultGainCalcDrivesMap",
            "ResultSamplingConfig",
            "GroupGainMapPtr",
            "GainSTMMode",
            "Drive",
            "LoopBehavior",
            "Segment",
            "ResultFociSTM",
            "FociSTMPtr",
            "ResultGainSTM",
            "GainSTMPtr",
            "DebugTypeWrap",
            "TransitionModeWrap",
            "SilencerTarget",
        ];
        let holo_ty = vec!["ResultBackend", "BackendPtr", "EmissionConstraintWrap"];
        if crate_name != "autd3capi-def"
            && used_ty
                .iter()
                .filter(|ty| def_ty.contains(&ty.as_str()))
                .next()
                .is_some()
        {
            writeln!(
                w,
                r"from pyautd3.native_methods.autd3capi_driver import {}
",
                used_ty
                    .iter()
                    .filter(|ty| def_ty.contains(&ty.as_str()))
                    .sorted()
                    .join(", ")
            )?;
        }
        if crate_name != "autd3capi-gain-holo"
            && used_ty
                .iter()
                .filter(|ty| holo_ty.contains(&ty.as_str()))
                .next()
                .is_some()
        {
            writeln!(
                w,
                r"from pyautd3.native_methods.autd3capi_gain_holo import {}
",
                used_ty
                    .iter()
                    .filter(|ty| holo_ty.contains(&ty.as_str()))
                    .sorted()
                    .join(", ")
            )?;
        }

        if !self.enums.is_empty() {
            writeln!(
                w,
                r"from enum import IntEnum
"
            )?;
        }

        self.enums
            .iter()
            .map(|e| {
                writeln!(
                    w,
                    r"
class {}(IntEnum):",
                    e.name
                )?;

                e.values
                    .iter()
                    .map(|(i, v)| writeln!(w, r"    {} = {}", Self::sub_reserve(i), v))
                    .try_collect()?;

                writeln!(
                    w,
                    r"
    @classmethod
    def from_param(cls, obj):
        return int(obj)  # pragma: no cover
"
                )
            })
            .try_collect()?;

        self.structs
            .iter()
            .filter(|e| e.name.ends_with("Ptr"))
            .map(|p| {
                writeln!(
                    w,
                    r"
class {}(ctypes.Structure):",
                    p.name
                )?;

                writeln!(
                    w,
                    "    _fields_ = [(\"_0\", ctypes.c_void_p)]
"
                )
            })
            .try_collect()?;

        // TODO: Resolve dependencies and define unions and structs in the correct order
        self.unions
            .iter()
            .filter(|u| u.name != "STMConfigValue")
            .map(|u| {
                writeln!(
                    w,
                    r"
class {}(ctypes.Union):",
                    u.name
                )?;
                writeln!(
                    w,
                    "    _fields_ = [{}]
",
                    u.values
                        .iter()
                        .map(|(name, ty)| format!("(\"{}\", {})", name, Self::to_return_ty(ty)))
                        .join(", ")
                )
            })
            .try_collect()?;

        self.structs
            .iter()
            .filter(|u| u.name != "STMConfigWrap")
            .filter(|e| !e.name.ends_with("Ptr"))
            .map(|p| {
                writeln!(
                    w,
                    r"
class {}(ctypes.Structure):",
                    p.name
                )?;

                writeln!(
                    w,
                    "    _fields_ = [{}]
",
                    p.fields
                        .iter()
                        .map(|(ty, name)| format!("(\"{}\", {})", name, Self::to_return_ty(ty)))
                        .join(", ")
                )?;
                writeln!(
                    w,
                    "
    def __eq__(self, other: object) -> bool:
        return isinstance(other, {}) and self._fields_ == other._fields_ # pragma: no cover
                    ",
                    p.name
                )
            })
            .try_collect()?;

        self.unions
            .iter()
            .filter(|u| u.name == "STMConfigValue")
            .map(|u| {
                writeln!(
                    w,
                    r"
class {}(ctypes.Union):",
                    u.name
                )?;
                writeln!(
                    w,
                    "    _fields_ = [{}]
",
                    u.values
                        .iter()
                        .map(|(name, ty)| format!("(\"{}\", {})", name, Self::to_return_ty(ty)))
                        .join(", ")
                )
            })
            .try_collect()?;

        self.structs
            .iter()
            .filter(|u| u.name == "STMConfigWrap")
            .map(|p| {
                writeln!(
                    w,
                    r"
class {}(ctypes.Structure):",
                    p.name
                )?;

                writeln!(
                    w,
                    "    _fields_ = [{}]
",
                    p.fields
                        .iter()
                        .map(|(ty, name)| format!("(\"{}\", {})", name, Self::to_return_ty(ty)))
                        .join(", ")
                )?;
                writeln!(
                    w,
                    "
    def __eq__(self, other: object) -> bool:
        return isinstance(other, {}) and self._fields_ == other._fields_ # pragma: no cover
                    ",
                    p.name
                )
            })
            .try_collect()?;

        self.constants
            .iter()
            .map(|constant| {
                write!(
                    w,
                    r"
{}: {} = {}
",
                    constant.name,
                    Self::to_python_ty(&constant.ty),
                    constant.value
                )
            })
            .try_collect()?;

        if crate_name == "autd3capi-driver" {
            writeln!(w)?;
            return Ok(());
        }

        write!(
            w,
            r"

class Singleton(type):
    _instances = {{}}  # type: ignore
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances: # pragma: no cover
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class NativeMethods(metaclass=Singleton):",
        )?;

        write!(
            w,
            r"

    def init_dll(self, bin_location: str, bin_prefix: str, bin_ext: str):
        try:
            self.dll = ctypes.CDLL(os.path.join(bin_location, f'{{bin_prefix}}{}{{bin_ext}}'))
        except Exception:   # pragma: no cover
            return          # pragma: no cover",
            crate_name.replace('-', "_")
        )?;

        self.functions
            .iter()
            .map(|function| {
                writeln!(w)?;
                let args = function.args.iter().map(Self::to_arg).join(", ");
                write!(
                    w,
                    r"
        self.dll.{}.argtypes = [{}]{}",
                    function.name,
                    args,
                    if function
                        .args
                        .iter()
                        .any(|arg| matches!(arg.ty, Type::Custom(_)))
                    {
                        "  # type: ignore"
                    } else {
                        ""
                    }
                )?;
                write!(
                    w,
                    r" 
        self.dll.{}.restype = {}",
                    function.name,
                    Self::to_return_ty(&function.return_ty)
                )
            })
            .try_collect()?;

        self.functions
            .iter()
            .map(|function| {
                writeln!(w)?;
                let args = function
                    .args
                    .iter()
                    .map(|arg| {
                        format!(
                            "{}: {}",
                            Self::sub_reserve(&arg.name),
                            Self::to_python_arg(arg)
                        )
                    })
                    .join(", ");
                let arg_names = function
                    .args
                    .iter()
                    .map(|arg| Self::sub_reserve(&arg.name))
                    .join(", ");

                write!(
                    w,
                    r"
    def {}(self{}{}) -> {}:
        return self.dll.{}({}){}",
                    Self::to_python_func_name(&function.name),
                    if function.args.is_empty() { "" } else { ", " },
                    args,
                    if function.return_ty == Type::Void {
                        "None".to_string()
                    } else {
                        Self::to_return_ty(&function.return_ty)
                    },
                    function.name,
                    arg_names,
                    if Self::to_python_func_name(&function.name).ends_with("t_4010_a_1") {
                        "  # pragma: no cover"
                    } else {
                        ""
                    }
                )
            })
            .try_collect()?;

        writeln!(w)?;

        Ok(())
    }
}
