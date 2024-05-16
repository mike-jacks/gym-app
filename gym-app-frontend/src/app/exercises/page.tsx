"use client";
import { useCallback, useEffect, useState } from "react";
import Layout from "../components/Layout";
import { fetchExercises } from "../utils/api";
import ExerciseCard from "../components/ExerciseCard";

interface Exercise {
  uuid: string;
  name: string;
  description: string;
  workout_category: string;
  movement_category: string;
  equipment: string;
  major_muscle: string;
  specific_muscles: string[];
  image_url: string;
}

const Exercises: React.FC = () => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [filteredExercises, setFilteredExercises] = useState<Exercise[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [nameFilter, setNameFilter] = useState("");
  const [workoutCategoryFilter, setWorkoutCategoryFilter] = useState("");
  const [movementCategoryFilter, setMovementCategoryFilter] = useState("");
  const [equipmentFilter, setEquipmentFilter] = useState("");
  const [majorMuscleFilter, setMajorMuscleFilter] = useState("");
  const [specificMuscleFilters, setSpecificMuscleFilters] = useState<string[]>([]);

  const handleToggle = (id: string) => {
    setExpandedId((prevId) => (prevId === id ? null : id));
  };

  const handleSpecificMuscleChange = (muscle: string) => {
    setSpecificMuscleFilters((prev) => (prev.includes(muscle) ? prev.filter((m) => m !== muscle) : [...prev, muscle]));
  };

  const filterExercises = useCallback(() => {
    let filtered = exercises;

    if (nameFilter) {
      filtered = filtered.filter((exercise) => exercise.name.toLowerCase().includes(nameFilter.toLowerCase()));
    }
    if (workoutCategoryFilter) {
      filtered = filtered.filter((exercise) => exercise.workout_category.toLowerCase().includes(workoutCategoryFilter.toLowerCase()));
    }
    if (movementCategoryFilter) {
      filtered = filtered.filter((exercise) => exercise.movement_category.toLowerCase().includes(movementCategoryFilter.toLowerCase()));
    }
    if (equipmentFilter) {
      filtered = filtered.filter((exercise) => exercise.equipment.toLowerCase().includes(equipmentFilter.toLowerCase()));
    }
    if (majorMuscleFilter) {
      filtered = filtered.filter((exercise) => exercise.major_muscle.toLowerCase().includes(majorMuscleFilter.toLowerCase()));
    }
    if (specificMuscleFilters.length > 0) {
      filtered = filtered.filter((exercise) => specificMuscleFilters.every((muscle) => exercise.specific_muscles.includes(muscle)));
    }

    setFilteredExercises(filtered);
  }, [exercises, nameFilter, workoutCategoryFilter, movementCategoryFilter, equipmentFilter, majorMuscleFilter, specificMuscleFilters]);

  useEffect(() => {
    const getExercises = async () => {
      try {
        const response = await fetchExercises();
        setExercises(response.data);
        setFilteredExercises(response.data);
      } catch (err) {
        setError("Failed to fetch exercises");
        console.error(err);
      }
    };

    getExercises();
  }, []);

  useEffect(() => {
    filterExercises();
  }, [filterExercises]);

  const uniqueWorkoutCategories = [...new Set(exercises.map((exercise) => exercise.workout_category))];
  const uniqueMovementCategories = [...new Set(exercises.map((exercise) => exercise.movement_category))];
  const uniqueEquipment = [...new Set(exercises.map((exercise) => exercise.equipment))];
  const uniqueMajorMuscles = [...new Set(exercises.map((exercise) => exercise.major_muscle))];
  const uniqueSpecificMuscles = [...new Set(exercises.flatMap((exercise) => exercise.specific_muscles || []))];

  return (
    <Layout>
      <h2 className="text-2xl mb-10 text-center">Exercises</h2>
      {error && <p className="text-red-500">{error}</p>}
      <div className="flex flex-col mb-4 p-4 bg-gray-800 rounded-lg">
        <div className="mb-4">
          <label className="block text-white mb-1" htmlFor="nameFilter">
            Search by name:
          </label>
          <input
            id="nameFilter"
            type="text"
            placeholder="Search by name"
            value={nameFilter}
            onChange={(e) => setNameFilter(e.target.value)}
            className="p-2 border border-gray-600 rounded bg-gray-700 text-white placeholder-gray-400 w-full"
          />
        </div>
        <div className="mb-4">
          <label className="block text-white mb-1" htmlFor="workoutCategoryFilter">
            Filter by workout category:
          </label>
          <select
            id="workoutCategoryFilter"
            value={workoutCategoryFilter}
            onChange={(e) => setWorkoutCategoryFilter(e.target.value)}
            className="p-2 border border-gray-600 rounded bg-gray-700 text-white w-full"
          >
            <option value="">All</option>
            {uniqueWorkoutCategories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-white mb-1" htmlFor="movementCategoryFilter">
            Filter by movement category:
          </label>
          <select
            id="movementCategoryFilter"
            value={movementCategoryFilter}
            onChange={(e) => setMovementCategoryFilter(e.target.value)}
            className="p-2 border border-gray-600 rounded bg-gray-700 text-white w-full"
          >
            <option value="">All</option>
            {uniqueMovementCategories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-white mb-1" htmlFor="equipmentFilter">
            Filter by equipment:
          </label>
          <select
            id="equipmentFilter"
            value={equipmentFilter}
            onChange={(e) => setEquipmentFilter(e.target.value)}
            className="p-2 border border-gray-600 rounded bg-gray-700 text-white w-full"
          >
            <option value="">All</option>
            {uniqueEquipment.map((equipment) => (
              <option key={equipment} value={equipment}>
                {equipment}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label className="block text-white mb-1" htmlFor="majorMuscleFilter">
            Filter by major muscle:
          </label>
          <select
            id="majorMuscleFilter"
            value={majorMuscleFilter}
            onChange={(e) => setMajorMuscleFilter(e.target.value)}
            className="p-2 border border-gray-600 rounded bg-gray-700 text-white w-full"
          >
            <option value="">All</option>
            {uniqueMajorMuscles.map((muscle) => (
              <option key={muscle} value={muscle}>
                {muscle}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-col items-center w-full">
          <p className="text-white mb-2">Filter by specific muscles:</p>
          <div className="grid lg:grid-rows-3 grid-rows-9 grid-flow-col gap-2 justify-center">
            {uniqueSpecificMuscles.map((muscle) => (
              <label key={muscle} className="flex items-center text-white">
                <input
                  type="checkbox"
                  checked={specificMuscleFilters.includes(muscle)}
                  onChange={() => handleSpecificMuscleChange(muscle)}
                  className="mr-2"
                />
                {muscle}
              </label>
            ))}
          </div>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {filteredExercises.map((exercise) => (
          <ExerciseCard key={exercise.uuid} isExpanded={expandedId === exercise.uuid} onToggle={() => handleToggle(exercise.uuid)} {...exercise} />
        ))}
      </div>
    </Layout>
  );
};

export default Exercises;
