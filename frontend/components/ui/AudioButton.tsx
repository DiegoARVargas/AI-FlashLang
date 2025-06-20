"use client";

import { useRef } from "react";

interface AudioButtonProps {
  src: string;
  size?: number;
}

export default function AudioButton({ src, size = 24 }: AudioButtonProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  return (
    <button
      onClick={() => audioRef.current?.play()}
      className="text-purple-400 hover:text-purple-300 transition duration-200"
    >
      <svg
        width={size}
        height={size}
        viewBox="0 0 100 100"
        fill="currentColor"
        xmlns="http://www.w3.org/2000/svg"
        className="drop-shadow-[0_0_6px_#a855f7]"
      >
        <polygon points="20,10 80,50 20,90" />
      </svg>
      <audio ref={audioRef} src={src} />
    </button>
  );
}
