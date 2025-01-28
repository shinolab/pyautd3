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
    match item {
        syn::Item::Struct(ItemStruct { attrs, .. })
        | syn::Item::Enum(ItemEnum { attrs, .. })
        | syn::Item::Union(ItemUnion { attrs, .. }) => attrs.iter().any(|attr| {
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
        }),
        syn::Item::Const(ItemConst { ty, .. }) => match **ty {
            syn::Type::Path(ref ty) => {
                ty.path.is_ident("i8")
                    || ty.path.is_ident("i16")
                    || ty.path.is_ident("i32")
                    || ty.path.is_ident("i64")
                    || ty.path.is_ident("u8")
                    || ty.path.is_ident("u16")
                    || ty.path.is_ident("u32")
                    || ty.path.is_ident("u64")
                    || ty.path.is_ident("f32")
                    || ty.path.is_ident("f64")
            }
            _ => false,
        },
        syn::Item::Fn(_) => true,
        _ => false,
    }
}
