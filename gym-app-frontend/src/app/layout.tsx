"use client";
import "./styles/globals.css";
import Header from "../app/components/Header";
import Footer from "../app/components/Footer";
import { AuthProvider } from "../app/components/AuthContext";

const RootLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AuthProvider>
    <html lang="en" className="dark">
      <body className="text-slate-200 bg-gradient-to-b from-green-900 to-blue-950">
        <Header />
        <div id="page-container">
          <main className="flex-grow container mx-auto p-4 mt-20">{children}</main>
          <Footer />
        </div>
      </body>
    </html>
  </AuthProvider>
);

export default RootLayout;
