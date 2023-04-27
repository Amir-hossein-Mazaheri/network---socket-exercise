import axios from "axios";

async function refreshNodes() {
  const res = await axios.get(
    import.meta.env.DEV
      ? "http://localhost:5500/refresh-nodes"
      : "/refresh-nodes"
  );

  return res.data as string[];
}

export default refreshNodes;
