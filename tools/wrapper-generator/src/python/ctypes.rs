use syn::__private::ToTokens;

#[derive(Debug)]
pub struct CtypesType(pub String);

impl TryFrom<syn::Type> for CtypesType {
    type Error = anyhow::Error;

    fn try_from(value: syn::Type) -> Result<Self, Self::Error> {
        match value {
            syn::Type::Array(syn::TypeArray { elem, len, .. }) => CtypesType::try_from(*elem)
                .map(|inner| CtypesType(format!("{} * {}", inner.0, len.to_token_stream()))),
            syn::Type::Paren(syn::TypeParen { elem, .. }) => CtypesType::try_from(*elem),
            syn::Type::Path(syn::TypePath { qself, path }) => {
                if qself.is_some() {
                    anyhow::bail!(
                        "Unsupported Path type: {:?}",
                        syn::TypePath { qself, path }.to_token_stream()
                    )
                }
                Ok(CtypesType(
                    match path.into_token_stream().to_string().as_str() {
                        "bool" => "ctypes.c_bool",
                        "char" | "c_char" => "ctypes.c_char",
                        "f32" => "ctypes.c_float",
                        "f64" => "ctypes.c_double",
                        "i8" => "ctypes.c_int8",
                        "i16" => "ctypes.c_int16",
                        "i32" => "ctypes.c_int32",
                        "i64" => "ctypes.c_int64",
                        "u8" => "ctypes.c_uint8",
                        "u16" => "ctypes.c_uint16",
                        "u32" => "ctypes.c_uint32",
                        "u64" => "ctypes.c_uint64",
                        "isize" | "usize" => {
                            anyhow::bail!("isize and usize are not supported")
                        }
                        "NonZeroU8" => "ctypes.c_uint8",
                        "NonZeroU16" => "ctypes.c_uint16",
                        "NonZeroU32" => "ctypes.c_uint32",
                        "NonZeroU64" => "ctypes.c_uint64",
                        "libc :: c_void" => "void",
                        "ConstPtr" => "ctypes.c_void_p",
                        v => v,
                    }
                    .to_owned(),
                ))
            }
            syn::Type::Ptr(syn::TypePtr { elem, .. }) => {
                CtypesType::try_from(*elem).map(|inner| match inner.0.as_str() {
                    "void" => CtypesType("ctypes.c_void_p".to_owned()),
                    "ctypes.c_char" => CtypesType("ctypes.c_char_p".to_owned()),
                    v => CtypesType(format!("ctypes.POINTER({})", v)),
                })
            }
            _ => anyhow::bail!("Unsupported type: {:?}", value.to_token_stream()),
        }
    }
}

impl TryFrom<syn::ReturnType> for CtypesType {
    type Error = anyhow::Error;

    fn try_from(value: syn::ReturnType) -> Result<Self, Self::Error> {
        match value {
            syn::ReturnType::Default => Ok(CtypesType("None".to_owned())),
            syn::ReturnType::Type(_, ty) => CtypesType::try_from(*ty),
        }
    }
}
