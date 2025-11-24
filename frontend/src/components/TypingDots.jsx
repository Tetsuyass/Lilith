import { useState, useEffect } from "react";

function TypingDots() {
  const [dots, setDots] = useState(".");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prev => (prev === "..." ? "." : prev + "."));
    }, 400);

    return () => clearInterval(interval);
  }, []);

  return <span>{dots}</span>;
}

export default TypingDots;
