use std::collections::HashMap;

use itertools::Itertools;

use crate::parser::Struct;

use super::CtypesType;

impl Struct {
    pub fn to_python_def(&self) -> anyhow::Result<String> {
        Ok(format!(
            r"class {}(ctypes.Structure):
    _fields_ = [{}]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, {0}) and self._fields_ == other._fields_  # pragma: no cover",
            self.name,
            self.fields
                .iter()
                .map(|(name, ty)| anyhow::Ok(format!(
                    "(\"{}\", {})",
                    name,
                    CtypesType::try_from(ty.clone())?.0
                )))
                .collect::<Result<Vec<_>, _>>()?
                .join(", ")
        ))
    }
}

pub fn sort_structs(structs: &[Struct], defined: Vec<String>) -> anyhow::Result<Vec<Struct>> {
    let mut structs = structs.to_vec();
    let deps = structs
        .iter()
        .map(|s| {
            let fields = s
                .fields
                .iter()
                .map(|(_, ty)| anyhow::Ok(CtypesType::try_from(ty.clone())?.0))
                .collect::<Result<Vec<_>, _>>()?
                .into_iter()
                .filter_map(|field| {
                    if field.starts_with("ctypes.") || defined.contains(&field) {
                        None
                    } else {
                        Some(field)
                    }
                })
                .collect::<Vec<_>>();
            anyhow::Ok((s.name.clone(), fields))
        })
        .collect::<Result<HashMap<_, _>, _>>()?;

    let mut sorted: Vec<Struct> = vec![];
    loop {
        let mut some_changed = false;
        for (name, fields) in deps.iter() {
            if let Some(idx) = structs.iter().position(|s| s.name == *name) {
                if fields.is_empty() || fields.iter().all(|f| sorted.iter().any(|s| s.name == *f)) {
                    sorted.push(structs.remove(idx));
                    some_changed = true;
                }
            }
        }

        if structs.is_empty() {
            break;
        }
        if !some_changed {
            tracing::error!(
                "Unresolved dependencies found: {:?}",
                structs
                    .iter()
                    .map(|s| format!(
                        "{}: {}",
                        s.name,
                        s.fields
                            .iter()
                            .map(|(_, ty)| CtypesType::try_from(ty.clone()).unwrap().0)
                            .join(", ")
                    ))
                    .join("\n")
            );

            anyhow::bail!("Unresolved dependencies found");
        }
    }

    Ok(sorted)
}
