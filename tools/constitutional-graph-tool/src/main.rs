use mlua::{Lua, Table, Value};
use serde_json::{json, Value as Json};
use std::fs;
use std::path::Path;

fn lua_to_json(lua: &Lua, value: Value) -> Json {
    match value {
        Value::Nil => Json::Null,
        Value::Boolean(b) => Json::Bool(b),
        Value::Integer(i) => Json::Number(i.into()),
        Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Json::Number(i.into())
            } else if let Some(f) = n.as_f64() {
                Json::Number(serde_json::Number::from_f64(f).unwrap_or(serde_json::Number::from(0)))
            } else {
                Json::Null
            }
        }
        Value::String(s) => Json::String(s.to_str().unwrap_or("").to_string()),
        Value::Table(t) => {
            let mut map = serde_json::Map::new();
            for pair in t.pairs::<String, Value>() {
                if let Ok((k, v)) = pair {
                    map.insert(k, lua_to_json(lua, v));
                }
            }
            Json::Object(map)
        }
        Value::Array(arr) => {
            let mut list = Vec::new();
            for v in arr.iter() {
                list.push(lua_to_json(lua, v.unwrap_or(Value::Nil)));
            }
            Json::Array(list)
        }
        _ => Json::Null,
    }
}

fn main() {
    let out_path = Path::new("data/graph_data.lua");
    let lua = Lua::new();

    let graph_data: Table = lua.load(out_path).call(()).expect("load graph_data.lua");
    let nodes: Vec<Json> = graph_data
        .get::<Table>("nodes")
        .expect("nodes table")
        .sequence_values::<Value>()
        .filter_map(|v| v.ok())
        .map(|v| lua_to_json(&lua, v))
        .collect();

    let edges: Vec<Vec<String>> = graph_data
        .get::<Table>("edges")
        .expect("edges table")
        .sequence_values::<Vec<String>>()
        .filter_map(|v| v.ok())
        .collect();

    let state_rows: Vec<Vec<String>> = graph_data
        .get::<Table>("state_rows")
        .expect("state_rows table")
        .sequence_values::<Vec<String>>()
        .filter_map(|v| v.ok())
        .collect();

    let source_map: serde_json::Map<String, Json> = graph_data
        .get::<Table>("source_map")
        .expect("source_map table")
        .pairs::<String, String>()
        .filter_map(|pair| pair.ok())
        .map(|(k, v)| (k, Json::String(v)))
        .collect();

    let payload = json!({
        "nodes": nodes,
        "edges": edges,
        "stateRows": state_rows,
        "sourceMap": source_map,
    });

    let data_json = serde_json::to_string_pretty(&payload).expect("serialize graph json");
    fs::write("target/graph_data.json", data_json).expect("write graph_data.json");

    let html = include_str!("../templates/index.html");
    let final_html = html.replace("{{GRAPH_DATA_JSON}}", &payload.to_string());
    fs::write("target/constitutional-semantic-graph.html", final_html).expect("write html");
    println!("wrote target/constitutional-semantic-graph.html");
}
