use syn::Type;
use syn::__private::ToTokens;

pub struct Const {
    pub name: String,
    pub ty: Type,
    pub value: String,
}

pub fn parse_const(item: &syn::Item) -> Option<Const> {
    if let syn::Item::Const(syn::ItemConst {
        ident, ty, expr, ..
    }) = item
    {
        let name = ident.to_string();
        Some(Const {
            name,
            ty: *ty.clone(),
            value: expr.to_token_stream().to_string(),
        })
    } else {
        None
    }
}
