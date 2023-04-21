import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import FileExplorer from "./components/FileExplorer";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <FileExplorer />
    </QueryClientProvider>
  );
}

export default App;
