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
    <header className="flex flex-col bg-slate-700 text-slate-300 p-4 fixed top-0 left-0 right-0 z-50 rounded-md mx-1">
      <h1 className="text-xl">Gym App</h1>
      <nav className="">
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
