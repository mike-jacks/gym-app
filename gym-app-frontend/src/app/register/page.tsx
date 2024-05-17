"use client";
// src/app/register/page.tsx
import { useState } from "react";
import { useRouter } from "next/navigation";
import Layout from "../components/Layout";
import { register } from "../utils/api";
import { RegistrationDataInput } from "../utils/interfaces";

function newDate() {
  return new Date().toISOString().split("T")[0];
}

const Register: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState<RegistrationDataInput>({
    first_name: "",
    last_name: "",
    birthday: newDate(),
    body_weight: 0,
    height: 0,
    gender: "male",
    username: "",
    hashed_password: "",
  });
  const [error, setError] = useState("");
  const [errorDescription, setErrorDescription] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  function handleDateChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    if (name === "birthday") {
      // This ensures the ISO string is split and only the date part (YYYY-MM-DD) is saved.
      let formattedDate = value.split("T")[0];
      setFormData((prevData) => ({
        ...prevData,
        [name]: formattedDate,
      }));
    } else {
      handleChange(event);
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await register(formData);
      alert("Registration successful with username: " + response.data.username);
      router.push("/login");
    } catch (err: any) {
      setError("Registration failed");
      setErrorDescription(err.detail);
      console.log(err.detail);
    }
  };

  return (
    <Layout>
      <div className="flex justify-center max-h-fit">
        <div className="border-2 border-slate-400 rounded-xl pb-20 pt-10 bg-gradient-to-br from-slate-800 to-slate-450 p-0 m-0 w-full max-w-xl">
          <h2 className="text-2xl mb-10 text-center">Register</h2>
          <form onSubmit={handleSubmit} className="flex flex-col items-center px-10">
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="first_name" className="mb-1 text-left">
                First Name:
              </label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                placeholder="First Name"
                value={formData.first_name}
                onChange={handleChange}
                className="p-2 border w-full text-gray-800 rounded-lg"
                required
              />
            </div>
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="last_name" className="mb-1 text-left">
                Last Name:
              </label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                placeholder="Last Name"
                value={formData.last_name}
                onChange={handleChange}
                className="p-2 border w-full text-gray-800 rounded-lg"
                required
              />
            </div>
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="birthday" className="mb-1 text-left">
                Birthday:
              </label>
              <input
                type="date"
                id="birthday"
                name="birthday"
                placeholder="Birthday"
                value={formData.birthday}
                onChange={handleDateChange}
                className="p-2 border w-full text-gray-800 rounded-lg"
                required
              />
            </div>
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="body_weight" className="mb-1 text-left">
                Body Weight (lb):
              </label>
              <input
                type="number"
                id="body_weight"
                name="body_weight"
                placeholder="Body Weight (lb)"
                value={formData.body_weight}
                onChange={handleChange}
                className="p-2 border w-full text-gray-800 rounded-lg"
                required
              />
            </div>
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="height" className="mb-1 text-left">
                Height (in):
              </label>
              <input
                type="number"
                id="height"
                name="height"
                placeholder="Height (in)"
                value={formData.height}
                onChange={handleChange}
                className="p-2 border w-full text-gray-800"
                required
              />
            </div>
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="gender" className="mb-1 text-left">
                Gender:
              </label>
              <select
                id="gender"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="p-2 border w-full  text-gray-800 rounded-lg"
                required
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="username" className="mb-1 text-left">
                Username:
              </label>
              <input
                type="text"
                id="username"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                className="p-2 border w-full text-gray-800 rounded-lg"
                required
              />
            </div>
            <div className="flex flex-col w-full mb-3">
              <label htmlFor="hashed_password">
                Password:
                <input
                  type="password"
                  id="hashed_password"
                  name="hashed_password"
                  placeholder="Password"
                  value={formData.hashed_password}
                  onChange={handleChange}
                  className="p-2 border w-full mb-3 text-gray-800 rounded-lg"
                  required
                />
              </label>
            </div>
            <button type="submit" className="p-2 bg-blue-800 text-gray-300 mt-2 w-full rounded-xl">
              Register
            </button>
            {error && <p className="text-red-500 text-center mt-2">{error}</p>}
            {errorDescription && <p className="text-red-500 text-center mt-2">{errorDescription}</p>}
          </form>
        </div>
      </div>
    </Layout>
  );
};

export default Register;
