use syn::Type;

#[derive(Clone)]
pub struct Struct {
    pub name: String,
    pub fields: Vec<(String, Type)>,
}

pub fn parse_struct(item: &syn::Item) -> Option<Struct> {
    if let syn::Item::Struct(syn::ItemStruct { ident, fields, .. }) = item {
        let name = ident.to_string();
        let fields = fields
            .into_iter()
            .map(|field| {
                let name = field
                    .ident
                    .as_ref()
                    .map(|x| x.to_string())
                    .unwrap_or_else(|| "value".to_string());
                (name, field.ty.clone())
            })
            .collect();
        Some(Struct { name, fields })
    } else {
        None
    }
}
