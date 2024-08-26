import { useDarkMode } from '../contexts/DarkModeContext';

export default function Navbar() {
  const { isDarkMode, toggleDarkMode } = useDarkMode();

  return (
    <nav className="bg-gray-800 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* ... existing navbar content ... */}
          <button
 