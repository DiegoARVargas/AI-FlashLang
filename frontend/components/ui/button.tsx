import React from "react";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

export const Button = ({ children, className = "", ...props }: ButtonProps) => {
  return (
    <button
      className={`bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-2xl transition ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};