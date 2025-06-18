"use client";

import Link from "next/link";
import { ReactNode } from "react";
import clsx from "clsx";

interface ElectricButtonProps {
  href: string;
  children: ReactNode;
  className?: string;
}

export default function ElectricButton({ href, children, className }: ElectricButtonProps) {
  return (
    <Link
      href={href}
      className={clsx(
        "electric-hover relative text-white text-sm font-medium px-4 py-2",
        className
      )}
    >
      {children}
    </Link>
  );
}
