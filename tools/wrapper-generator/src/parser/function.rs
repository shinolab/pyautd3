use quote::ToTokens as _;
use syn::{ReturnType, Type};

pub struct Arg {
    pub name: String,
    pub ty: Type,
}

impl std::fmt::Debug for Arg {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}: {}", self.name, self.ty.to_token_stream())
    }
}

pub struct Function {
    pub name: String,
    pub return_ty: ReturnType,
    pub args: Vec<Arg>,
}

impl std::fmt::Debug for Function {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}({}){}",
            self.name,
            self.args
                .iter()
                .map(|arg| format!("{:?}", arg))
                .collect::<Vec<_>>()
                .join(", "),
            self.return_ty.to_token_stream()
        )
    }
}

pub fn parse_function(item: &syn::Item) -> Option<Function> {
    if let syn::Item::Fn(syn::ItemFn { sig, .. }) = item {
        let name = sig.ident.to_string();
        let return_ty = sig.output.clone();
        let args_ = sig
            .inputs
            .iter()
            .filter_map(|arg| match arg {
                syn::FnArg::Typed(syn::PatType { pat, ty, .. }) => {
                    let name = pat.to_token_stream().to_string().replace("mut ", "");
                    Some(Arg {
                        name,
                        ty: *ty.clone(),
                    })
                }
                _ => None,
            })
            .collect::<Vec<_>>();

        if sig.inputs.len() != args_.len() {
            tracing::info!("Skip fn {} because it has receiver arguments", name);
            return None;
        }

        Some(Function {
            name,
            return_ty,
            args: args_,
        })
    } else {
        None
    }
}
