use syn::MetaList;
use syn::__private::ToTokens;

#[derive(Clone)]
pub struct Enum {
    pub name: String,
    pub ty: syn::Type,
    pub variants: Vec<(String, String)>,
}

pub fn parse_enum(item: &syn::Item) -> Option<Enum> {
    if let syn::Item::Enum(syn::ItemEnum {
        ident,
        variants,
        attrs,
        ..
    }) = item
    {
        let name = ident.to_string();

        let ty = attrs.iter().find_map(|attr| {
            if attr.path().is_ident("repr") {
                match attr.meta.clone() {
                    syn::Meta::List(MetaList { tokens, .. }) => Some(tokens.to_string()),
                    _ => None,
                }
            } else {
                None
            }
        });

        if ty.is_none() {
            tracing::info!("Skip enum {} because it has no repr attribute", name);
            return None;
        };

        let ty = ty.unwrap();
        let ty: syn::Type = syn::parse_str(&ty).unwrap();

        let variants_ = variants
            .iter()
            .filter_map(|variant| {
                let name = variant.ident.to_string();
                let (_, expr) = variant.discriminant.as_ref()?;
                Some((name, expr.to_token_stream().to_string()))
            })
            .collect::<Vec<_>>();
        if variants.len() != variants_.len() {
            tracing::info!(
                "Skip enum {} because it has non-explicit discriminants",
                name
            );
            return None;
        }
        Some(Enum {
            name,
            ty,
            variants: variants_,
        })
    } else {
        None
    }
}
