import axios from "axios";

async function getNodes() {
  const res = await axios.get(
    import.meta.env.DEV ? "http://localhost:5500/nodes" : "/nodes"
  );

  return res.data as string[];
}

export default getNodes;
