import { useEffect, useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import FileExplorer from "./components/FileExplorer";
import SelectNode from "./components/SelectNode";

const queryClient = new QueryClient();

function App() {
  const [node, setNode] = useState("");
  const [showNodes, setShowNodes] = useState(true);

  useEffect(() => {
    localStorage.setItem("node", node);
  }, [node]);

  return (
    <QueryClientProvider client={queryClient}>
      {showNodes ? (
        <SelectNode node={node} setNode={setNode} setShowNodes={setShowNodes} />
      ) : (
        <FileExplorer setShowNodes={setShowNodes} />
      )}
    </QueryClientProvider>
  );
}

export default App;
