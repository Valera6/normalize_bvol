use serde::{Deserialize, Serialize};
use serde_json;
use std::collections::HashMap;
use std::fs;

#[derive(Debug, Serialize, Deserialize)]
struct Data(HashMap<String, f64>);

fn load_entries() -> Vec<u16> {
	let file_path = r"C:\Users\Valera\anaconda3\MyScripts\_Testing\Rust\normalize_bvol\data.json";

	let json_str = fs::read_to_string(file_path).expect("Unable to read the file");

	let parsed_data: Data = serde_json::from_str(&json_str).unwrap();
	let values_vec: Vec<f64> = parsed_data.0.values().cloned().collect();
	let entries: Vec<u16> = values_vec.iter().map(|&val| (val * 100.0) as u16).collect();
	entries
}

fn main() {
	let entries = load_entries();
	println!("len: {}", entries.len());
}
