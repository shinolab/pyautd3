mod r#const;
mod ctypes;
mod r#enum;
mod function;
mod r#struct;
mod r#union;

pub use ctypes::CtypesType;
pub use function::*;
use quote::ToTokens;
pub use r#struct::*;

pub struct PythonType(pub String);

impl TryFrom<syn::Type> for PythonType {
    type Error = anyhow::Error;

    fn try_from(value: syn::Type) -> Result<Self, Self::Error> {
        match value {
            syn::Type::Array(syn::TypeArray { elem, len, .. }) => PythonType::try_from(*elem)
                .map(|inner| PythonType(format!("{} * {}", inner.0, len.to_token_stream()))),
            syn::Type::Paren(syn::TypeParen { elem, .. }) => PythonType::try_from(*elem),
            syn::Type::Path(syn::TypePath { qself, path }) => {
                if qself.is_some() {
                    anyhow::bail!(
                        "Unsupported Path type: {:?}",
                        syn::TypePath { qself, path }.to_token_stream()
                    )
                }
                Ok(PythonType(
                    match path.into_token_stream().to_string().as_str() {
                        "f32" | "f64" => "float",
                        "i8" | "i16" | "i32" | "i64" | "u8" | "u16" | "u32" | "u64" => "int",
                        "isize" | "usize" => {
                            anyhow::bail!("isize and usize are not supported")
                        }
                        "ConstPtr" => "ctypes.c_void_p",
                        v => v,
                    }
                    .to_owned(),
                ))
            }
            syn::Type::Ptr(syn::TypePtr { elem, .. }) => match *elem {
                syn::Type::Ptr(syn::TypePtr { elem, .. }) => CtypesType::try_from(*elem)
                    .map(|inner| PythonType(format!("ctypes.Array[ctypes.Array[{}]]", inner.0))),
                elem => CtypesType::try_from(elem).map(|inner| match inner.0.as_str() {
                    "ctypes.c_char" => PythonType("bytes".to_owned()),
                    v => PythonType(format!("ctypes.Array[{}]", v)),
                }),
            },
            _ => anyhow::bail!("Unsupported type: {}", value.to_token_stream().to_string()),
        }
    }
}
