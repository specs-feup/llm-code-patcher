laraImport("weaver.Query");

for (const chain of Query.search("file")
  .search("function")
  .search("vardecl")
  .chain()) {
  console.log(
    chain["file"].name +
      " -> " +
      chain["function"].name +
      " -> " +
      chain["vardecl"].name +
      ":" +
      chain["vardecl"].type.code +
      "\n"
  );
}

console.log("-------------\n");

for (const chain of Query.search("file")
  .search("function")
  .search("varref")
  .chain()) {
  console.log(
    chain["file"].name +
      " -> " +
      chain["function"].name +
      " -> " +
      chain["varref"].name +
      ":" +
      chain["varref"].type.code
  );

  console.log("Type jp: " + chain["varref"].type.desugarAll.typeFields + "\n");
}

for (const s of Query.search("struct")) {
  console.log("Struct fields:\n");

  for (const f of s.fields) {
    console.log(f.name + " -> " + f.type.code);
  }
}

console.log(Query.root().ast);

console.log(Query.root().dump);
