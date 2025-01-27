use syn::{ItemConst, ItemEnum, ItemStruct, ItemUnion};

pub fn is_public_item(item: &syn::Item) -> bool {
    matches!(
        match item {
            syn::Item::Struct(ItemStruct { vis, .. })
            | syn::Item::Const(ItemConst { vis, .. })
            | syn::Item::Enum(ItemEnum { vis, .. })
            | syn::Item::Union(ItemUnion { vis, .. })
            | syn::Item::Fn(syn::ItemFn { vis, .. }) => vis,
            _ => return false,
        },
        syn::Visibility::Public(_)
    )
}

pub fn is_ffi_safe_item(item: &syn::Item) -> bool {
    let vec = match item {
        syn::Item::Struct(ItemStruct { attrs, .. })
        | syn::Item::Const(ItemConst { attrs, .. })
        | syn::Item::Enum(ItemEnum { attrs, .. })
        | syn::Item::Union(ItemUnion { attrs, .. }) => attrs,
        syn::Item::Fn(_) => return true,
        _ => return false,
    };
    let attrs = vec;
    attrs.into_iter().any(|attr| {
        if attr.path().is_ident("repr") {
            attr.parse_nested_meta(|meta| {
                if meta.path.is_ident("C") {
                    return Ok(());
                }
                if meta.path.is_ident("u8") {
                    return Ok(());
                }
                Err(meta.error(""))
            })
            .is_ok()
        } else {
            false
        }
    })
}
