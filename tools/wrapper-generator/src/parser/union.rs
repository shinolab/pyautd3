use syn::Type;

pub struct Union {
    pub name: String,
    pub fields: Vec<(String, Type)>,
}

pub fn parse_union(item: &syn::Item) -> Option<Union> {
    if let syn::Item::Union(syn::ItemUnion { ident, fields, .. }) = item {
        let name = ident.to_string();

        Some(Union {
            name,
            fields: fields
                .named
                .iter()
                .map(|field| {
                    let name = field.ident.clone().unwrap().to_string();
                    (name, field.ty.clone())
                })
                .collect::<Vec<_>>(),
        })
    } else {
        None
    }
}
