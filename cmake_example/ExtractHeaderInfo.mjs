laraImport("weaver.Query");

for (const f of Query.search("file", "math.h").search("function", n => !n.startsWith("_"))) {

  console.log(f.name + " -> " + f.type + "\n");
  const functionType = f.functionType;
//  console.log("F TYPE: " + functionType.joinPointType)
  console.log("Params: \n");
  for(const p of functionType.paramTypes) {
  	console.log(p.code + "\n");
  }
  console.log("Return: " + functionType.returnType.code + "\n");
}
