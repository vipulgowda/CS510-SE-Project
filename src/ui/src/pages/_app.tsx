import "@/styles/globals.css"; // ✅ Import Tailwind styles
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
