// mod parse;
mod parser;
mod python;
// mod types;
mod utils;

use std::env;
use std::fs::File;
use std::io::{BufWriter, Read as _, Write as _};
use std::path::Path;

use anyhow::Result;
use glob::glob;

use cargo_metadata::MetadataCommand;
use itertools::Itertools;
use parser::{Enum, Function, Struct, Union};
// use parse::*;
// use python::PythonGenerator;
use python::{escape_python_builtin, sort_structs, to_python_func_name, CtypesType, PythonType};
use utils::{is_ffi_safe_item, is_public_item};

// pub fn gen<P1: AsRef<Path>, P2: AsRef<Path>>(crate_path: P1, dest_dir: P2) -> Result<()> {
//     std::fs::create_dir_all(dest_dir.as_ref())?;

//     let metadata = MetadataCommand::new()
//         .manifest_path(crate_path.as_ref().join("Cargo.toml"))
//         .exec()?;

//     let crate_name = metadata.root_package().unwrap().name.as_str();

//     glob::glob(&format!(
//         "{}/**/*.rs",
//         crate_path.as_ref().join("src").display()
//     ))?
//     .try_fold(PythonGenerator::new(), |acc, path| -> Result<_> {
//         let path = path?;
//         Ok(acc
//             .register_enum(parse_enum(&path)?)
//             .register_struct(parse_struct(&path)?, false))
//     })?
//     .write(dest_dir, crate_name, false)
// }

// pub fn gen_capi<P1: AsRef<Path>, P2: AsRef<Path>>(crate_path: P1, dest_dir: P2) -> Result<()> {
//     std::fs::create_dir_all(dest_dir.as_ref())?;

//     let metadata = MetadataCommand::new()
//         .manifest_path(crate_path.as_ref().join("Cargo.toml"))
//         .exec()?;

//     let crate_name = metadata.root_package().unwrap().name.as_str();

//     glob::glob(&format!(
//         "{}/**/*.rs",
//         crate_path.as_ref().join("src").display()
//     ))?
//     .try_fold(PythonGenerator::new(), |acc, path| -> Result<_> {
//         let path = path?;
//         Ok(acc
//             .register_func(parse_func(&path)?)
//             .register_const(parse_const(&path)?)
//             .register_enum(parse_enum(&path)?)
//             .register_union(parse_union(&path)?)
//             .register_struct(parse_struct(&path)?, true))
//     })?
//     .write(dest_dir, crate_name, true)
// }

struct PythonWrapperGenerator {
    ignore_items: Vec<&'static str>,
}

impl PythonWrapperGenerator {
    fn parse(
        &self,
        root: impl AsRef<Path>,
    ) -> anyhow::Result<(Vec<Struct>, Vec<Enum>, Vec<Union>, Vec<Function>)> {
        let mut structs = vec![];
        let mut enums = vec![];
        let mut unions = vec![];
        let mut functions = vec![];

        for src in glob::glob(&format!("{}/**/*.rs", root.as_ref().join("src").display()))? {
            let mut file = std::fs::File::open(src?)?;
            let mut contents = String::new();
            file.read_to_string(&mut contents)?;

            let syntax_tree = syn::parse_file(&contents)?;
            syntax_tree.items.into_iter().for_each(|item| {
                if !matches!(
                    &item,
                    syn::Item::Struct(_)
                        | syn::Item::Enum(_)
                        | syn::Item::Union(_)
                        | syn::Item::Const(_)
                        | syn::Item::Fn(_)
                ) {
                    return;
                }

                if !is_public_item(&item) | !is_ffi_safe_item(&item) {
                    return;
                }
                if let Some(s) = parser::parse_struct(&item) {
                    if self.ignore_items.contains(&s.name.as_str()) {
                        return;
                    }
                    structs.push(s);
                }
                if let Some(e) = parser::parse_enum(&item) {
                    if self.ignore_items.contains(&e.name.as_str()) {
                        return;
                    }
                    enums.push(e);
                }
                if let Some(u) = parser::parse_union(&item) {
                    if self.ignore_items.contains(&u.name.as_str()) {
                        return;
                    }
                    unions.push(u);
                }
                if let Some(f) = parser::parse_function(&item) {
                    if self.ignore_items.contains(&f.name.as_str()) {
                        return;
                    }
                    functions.push(f);
                }
            });
        }

        Ok((structs, enums, unions, functions))
    }

    pub fn gen(
        &self,
        root: impl AsRef<Path>,
        defined: &mut Vec<(String, String)>,
    ) -> anyhow::Result<()> {
        let mut structs = vec![];
        let mut enums = vec![];
        for entry in glob(&format!("{}/autd3/*/Cargo.toml", root.as_ref().display()))? {
            let entry = entry?;
            let manifest_path = Path::new(&entry);

            let (s, e, _, _) = self.parse(manifest_path.parent().unwrap())?;
            structs.extend(s);
            enums.extend(e);
        }

        Self::write(root, "autd3", &structs, &enums, &[], &[], defined)?;

        Ok(())
    }

    pub fn gen_capi(
        &self,
        root: impl AsRef<Path>,
        manifest_path: impl AsRef<Path>,
        defined: &mut Vec<(String, String)>,
    ) -> anyhow::Result<()> {
        let metadata = MetadataCommand::new()
            .manifest_path(manifest_path.as_ref())
            .exec()?;
        let crate_name = metadata.root_package().unwrap().name.as_str();

        let (structs, enums, unions, functions) =
            self.parse(manifest_path.as_ref().parent().unwrap())?;

        Self::write(
            &root,
            &crate_name.replace("-", "_"),
            &structs,
            &enums,
            &unions,
            &functions,
            defined,
        )?;

        Ok(())
    }

    fn write<P: AsRef<Path>>(
        root: P,
        src: &str,
        structs: &[Struct],
        enums: &[Enum],
        unions: &[Union],
        functions: &[Function],
        defined: &mut Vec<(String, String)>,
    ) -> anyhow::Result<()> {
        let path = format!("pyautd3/native_methods/{}", src);
        let module_name = path.replace("/", ".").replace("\\", ".");
        let dst = root
            .as_ref()
            .parent()
            .unwrap()
            .parent()
            .unwrap()
            .join(format!("{}.py", path));
        let mut w = BufWriter::new(File::create(dst)?);

        if !functions.is_empty() {
            writeln!(w, "import threading")?;
            writeln!(w, "from pathlib import Path")?;
        }
        if !structs.is_empty() || !unions.is_empty() || !functions.is_empty() {
            writeln!(w, "import ctypes")?;
        }
        if !enums.is_empty() {
            writeln!(w, "import enum")?;
        }
        for (name, module) in defined.iter() {
            if structs.iter().any(|s| {
                s.fields.iter().any(|f| {
                    CtypesType::try_from(f.1.clone())
                        .is_ok_and(|t| &t.0 == name || t.0 == format!("ctypes.POINTER({})", name))
                })
            }) || unions.iter().any(|s| {
                s.fields.iter().any(|f| {
                    CtypesType::try_from(f.1.clone())
                        .is_ok_and(|t| &t.0 == name || t.0 == format!("ctypes.POINTER({})", name))
                })
            }) || functions.iter().any(|f| {
                f.args.iter().any(|a| {
                    CtypesType::try_from(a.ty.clone())
                        .is_ok_and(|t| &t.0 == name || t.0 == format!("ctypes.POINTER({})", name))
                })
            }) || functions.iter().any(|f| {
                CtypesType::try_from(f.return_ty.clone())
                    .is_ok_and(|t| &t.0 == name || t.0 == format!("ctypes.POINTER({})", name))
            }) {
                writeln!(w, "from {module} import {name}")?;
            }
        }

        for e in enums {
            writeln!(w, "\n\n{}", e.to_python_def()?)?;
        }
        defined.extend(enums.iter().map(|e| (e.name.clone(), module_name.clone())));

        for u in unions {
            writeln!(w, "\n\n{}", u.to_python_def()?)?;
        }
        defined.extend(unions.iter().map(|e| (e.name.clone(), module_name.clone())));

        for s in sort_structs(structs, defined.iter().map(|(n, _)| n.clone()).collect())? {
            writeln!(w, "\n\n{}", s.to_python_def()?)?;
        }
        defined.extend(
            structs
                .iter()
                .map(|s| (s.name.clone(), module_name.clone())),
        );

        if functions.is_empty() {
            return Ok(());
        }

        writeln!(
            w,
            r"
class Singleton(type):
    _instances = {{}}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances: # pragma: no cover
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class NativeMethods(metaclass=Singleton):
    def init_dll(self, bin_location: Path, bin_prefix: str, bin_ext: str) -> None:
        self.dll = ctypes.CDLL(str(bin_location / f'{{bin_prefix}}{}{{bin_ext}}'))",
            src
        )?;

        for f in functions {
            writeln!(
                w,
                r"
        self.dll.{}.argtypes = [{}]
        self.dll.{0}.restype = {}",
                f.name,
                f.to_python_def_arg()?,
                f.to_python_def_return()?
            )?;
        }

        for f in functions {
            writeln!(
                w,
                r"
    def {}(self{}{}) -> {}:
        return self.dll.{}({})",
                to_python_func_name(&f.name),
                if f.args.is_empty() { "" } else { ", " },
                f.args
                    .iter()
                    .map(|arg| Ok(format!(
                        "{}: {}",
                        escape_python_builtin(&arg.name),
                        PythonType::try_from(arg.ty.clone())?.0
                    )))
                    .collect::<Result<Vec<_>>>()?
                    .join(", "),
                f.to_python_def_return()?,
                f.name,
                f.args
                    .iter()
                    .map(|arg| escape_python_builtin(&arg.name))
                    .join(", ")
            )?;
        }

        Ok(())
    }
}

fn main() -> Result<()> {
    let home = env::var("CARGO_MANIFEST_DIR")?;

    tracing_subscriber::fmt::init();

    let mut defined = vec![
        (
            "Vector3".to_string(),
            "pyautd3.native_methods.structs".to_string(),
        ),
        (
            "Point3".to_string(),
            "pyautd3.native_methods.structs".to_string(),
        ),
        (
            "Quaternion".to_string(),
            "pyautd3.native_methods.structs".to_string(),
        ),
    ];

    PythonWrapperGenerator {
        ignore_items: vec![
            "RxMessage",
            "TxMessage",
            "ClkControlFlags",
            "GPIOInFlags",
            "ModulationControlFlags",
            "SilencerControlFlags",
            "GainControlFlags",
            "ControlPoints",
            "FociSTMControlFlags",
            "GainSTMControlFlags",
            "FirmwareVersionType",
        ],
    }
    .gen(&home, &mut defined)?;

    PythonWrapperGenerator {
        ignore_items: vec![],
    }
    .gen_capi(
        &home,
        &format!("{}/capi/autd3capi-driver/Cargo.toml", home),
        &mut defined,
    )?;

    for entry in glob(&format!("{}/capi/*/Cargo.toml", home))? {
        let entry = entry?;
        if entry.to_str().unwrap().contains("autd3capi-driver") {
            continue;
        }
        PythonWrapperGenerator {
            ignore_items: vec![
                "AUTDGainHoloGreedyT4010A1",
                "AUTDGainHoloGST4010A1",
                "AUTDGainHoloGSPATT4010A1",
                "AUTDGainHoloLMT4010A1",
                "AUTDGainHoloNaiveT4010A1",
                "AUTDNalgebraBackendT4010A1",
                "AUTDDeleteNalgebraBackendT4010A1",
            ],
        }
        .gen_capi(&home, &entry, &mut defined)?;
    }

    PythonWrapperGenerator {
        ignore_items: vec![],
    }
    .gen_capi(
        &home,
        &format!("{}/capi-emulator/Cargo.toml", home),
        &mut defined,
    )?;

    Ok(())
}
