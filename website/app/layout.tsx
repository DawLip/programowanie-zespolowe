
import { Inter } from 'next/font/google'
import type { Metadata } from "next";
import "./globals.css";
import { SocketProvider, useSocket } from './socket';

const roboto = Inter({
  weight: ['200', '300','400', '600','700'],
  style: ['normal'],
  subsets: ['latin'],
})
export const metadata: Metadata = {
  title: "ChatNow"
};
/**
 * Główny layout 
 * @param props - obiekt właściwości komponentu
 * @param props.children - elementy potomne renderowane w layoucie
 * @returns {JSX.Element} Layout
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children} 
      </body>
    </html>
  );
}
