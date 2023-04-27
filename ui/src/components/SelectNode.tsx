import { useQuery } from "@tanstack/react-query";

import getNodes from "../api/getNodes";
import refreshNodes from "../api/refreshNodes";

interface SelectNodeProps {
  node: string;
  setNode: (node: string) => void;
  setShowNodes: (showNodes: boolean) => void;
}

const SelectNode: React.FC<SelectNodeProps> = ({
  node,
  setNode,
  setShowNodes,
}) => {
  const { data, isFetching, refetch } = useQuery(["nodes"], getNodes);
  const { refetch: refresh, isFetching: isRefreshing } = useQuery(
    ["refresh-nodes"],
    refreshNodes,
    {
      enabled: false,
    }
  );

  const handleRefreshNodes = async () => {
    await refresh();
    await refetch();
  };

  const handleShowNodes = (node: string) => () => {
    setNode(node);
    setShowNodes(false);
  };

  return (
    <div className="px-12 py-8 bg-gray-800 text-white min-h-screen w-screen">
      <div className="mb-12 flex items-center justify-between">
        <h1 className="font-bold text-3xl">
          List of nodes you can select to get files from them:
        </h1>

        <div className="flex items-center gap-8">
          {!!node && (
            <div
              onClick={() => setShowNodes(false)}
              className="cursor-pointer font-bold border border-white rounded-full px-12 py-2"
            >
              Go Back to File Explorer
            </div>
          )}

          <button
            disabled={isRefreshing || isFetching}
            className="cursor-pointer font-bold text-gray-900 bg-white rounded-full px-12 py-2"
            onClick={handleRefreshNodes}
          >
            {isRefreshing || isFetching ? "Loading..." : "Refresh"}
          </button>
        </div>
      </div>

      {isFetching || isRefreshing ? (
        <p>Loading list of available nodes...</p>
      ) : (
        <ul className="grid grid-cols-3 gap-6">
          {data?.map((node) => (
            <li
              onClick={handleShowNodes(node)}
              className="cursor-pointer font-semibold px-6 py-3 border border-white rounded-full text-center hover:text-gray-700 hover:bg-white transition-colors duration-200"
            >
              {node}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default SelectNode;
