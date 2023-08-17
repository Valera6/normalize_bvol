use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;

#[derive(Debug, Serialize, Deserialize)]
struct Data(HashMap<String, f64>);

fn main() {
	let file_path = r"C:\Users\Valera\anaconda3\MyScripts\_Testing\Rust\normalize_bvol\data.json";

	let json_str = fs::read_to_string(file_path).expect("Unable to read the file");

	let parsed_data: Data = serde_json::from_str(&json_str).unwrap();
	println!("{:?}", parsed_data);
}
