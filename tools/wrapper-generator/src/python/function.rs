use convert_case::{Case, Casing};

use crate::parser::Function;

use super::CtypesType;

impl Function {
    pub fn to_python_def_arg(&self) -> anyhow::Result<String> {
        Ok(self
            .args
            .iter()
            .map(|arg| anyhow::Ok(CtypesType::try_from(arg.ty.clone())?.0))
            .collect::<Result<Vec<_>, _>>()?
            .join(", "))
    }

    pub fn to_python_def_return(&self) -> anyhow::Result<String> {
        Ok(CtypesType::try_from(self.return_ty.clone())?.0)
    }
}

pub fn to_python_func_name(name: &str) -> String {
    let name = name[4..].to_string();
    name.to_case(Case::Snake)
}

pub fn escape_python_builtin(name: &str) -> String {
    match name {
        "len" => "len_".to_string(),
        "dir" => "dir_".to_string(),
        "map" => "map_".to_string(),
        "range" => "range_".to_string(),
        _ => name.to_string(),
    }
}
