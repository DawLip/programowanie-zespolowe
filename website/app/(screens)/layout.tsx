"use client";

import { SocketProvider } from '../socket';

/**
 * Layout z providerem socket.io
 * @param props - obiekt właściwości komponentu
 * @param props.children - elementy potomne renderowane wewnątrz providera
 * @returns {JSX.Element} Layout
 */
export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SocketProvider>
      {children}
    </SocketProvider>
  );
}