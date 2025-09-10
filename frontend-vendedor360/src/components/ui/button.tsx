import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "ghost";
  className?: string;
}

export default function Button({
  variant = "default",
  className = "",
  ...props
}: ButtonProps) {
  const baseClasses =
    "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background px-4 py-2";
  const variantClasses =
    variant === "default"
      ? "bg-primary text-white hover:bg-primary/90"
      : "bg-transparent hover:bg-muted";
  return (
    <button
      className={`${baseClasses} ${variantClasses} ${className}`.trim()}
      {...props}
    />
  );
}
