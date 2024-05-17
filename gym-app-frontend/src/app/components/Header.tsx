import "@/app/styles/globals.css";
import Link from "next/link";
import { useAuth } from "./AuthContext";

export default function Header() {
  const { token, setToken } = useAuth();

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };
  return (
    <header className="bg-slate-700 text-slate-300 p-4 fixed top-0 w-full z-50 rounded-md mx-2 mt-1">
      <h1 className="text-xl">Gym App</h1>
      <nav className="w-full">
        <Link href="/">Home</Link> |{" "}
        {token ? (
          <>
            {" "}
            <Link onClick={handleLogout} href="/login">
              Logout
            </Link>{" "}
            | <Link href="/exercises">Exercises</Link>{" "}
          </>
        ) : (
          <>
            {" "}
            <Link href="/register">Register</Link> | <Link href="/login">Login</Link>{" "}
          </>
        )}
      </nav>
    </header>
  );
}
