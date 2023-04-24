import React, { useEffect, useRef } from "react";
import { useQuery } from "@tanstack/react-query";

import { TFileItem } from "../api/getList";
import getFile from "../api/getFile";

interface FileItemProps extends TFileItem {
  setPrefix: (prefix: string) => void;
}

const FileItem: React.FC<FileItemProps> = ({ name, path, type, setPrefix }) => {
  const anchorRef = useRef<HTMLAnchorElement>(null);

  const { data: res } = useQuery(["file-content", name], () => getFile(path));

  // normally I shouldn't use the 'useEffect' hook but there was a weird
  // and unsolvable bug with the event driven way so I switched
  useEffect(() => {
    if (type === "DIR" || !res || !anchorRef.current) return;

    anchorRef.current.href = `data:${
      res.headers["content-type"]
    };charset=utf-8,${encodeURIComponent(res.data)}`;

    anchorRef.current.download = name;
  }, [res, type, name]);

  return (
    <div
      onClick={() => type === "DIR" && setPrefix(path)}
      className="flex items-center gap-3 cursor-pointer"
    >
      {type === "DIR" ? (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0121.75 12v.75m-8.69-6.44l-2.12-2.12a1.5 1.5 0 00-1.061-.44H4.5A2.25 2.25 0 002.25 6v12a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9a2.25 2.25 0 00-2.25-2.25h-5.379a1.5 1.5 0 01-1.06-.44z"
          />
        </svg>
      ) : (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
          className="w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
          />
        </svg>
      )}
      <a ref={anchorRef}>{name}</a>
    </div>
  );
};

export default FileItem;
