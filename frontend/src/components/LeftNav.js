import React, { useContext } from "react";
import { AiOutlinePlus } from "react-icons/ai";
import { LuPanelLeftClose } from "react-icons/lu";
import { SlOptions } from "react-icons/sl";
import { ContextApp } from "../utils/Context";
function LeftNav() {
  const { setShowSlide, showSlide, clearMessages } = useContext(ContextApp);
  return (
    // top section
    <div
      className={
        !showSlide
          ? "h-screen bg-gray-900 w-[300px] border-r border-gray-500 hidden lg:flex items-center justify-between p-2 text-white flex-col translate-x-0"
          : "hidden"
      }
    >
      <div className="flex items-start justify-between w-full">
        <span
          className="border border-gray-600  rounded w-[80%] py-2 text-xs flex gap-1 items-center justify-center cursor-pointer"
          onClick={() => clearMessages()}
        >
          <AiOutlinePlus fontSize={18} />
          New Chat
        </span>
        <span
          className="border border-gray-600  rounded px-3 py-[9px] flex items-center justify-center cursor-pointer"
          title="Close sidebar"
          onClick={() => setShowSlide(!showSlide)}
        >
          <LuPanelLeftClose />
        </span>
      </div>
      {/* middle section  */}
   
      {/* bottom section  */}
      <div className="w-full border-t border-gray-600 flex flex-col gap-2 items-center justify-center p-2">
        <a
          href="https://www.linkedin.com/in/qutaiba-olayyan/"
          target="_blank"
          rel="noopener noreferrer"
          className="w-full"
        >
          <span className="rounded w-full py-2 px-2 text-xs flex gap-1 items-center justify-between cursor-pointer hover:bg-gray-800 transition-all duration-300">
            <span className="flex gap-2 items-center justify-center text-sm font-bold">
              <img
                src="/user.jpg"
                alt="user"
                className="w-8 h-8 object-cover rounded-sm"
              />
              Qutaiba Olayyan
            </span>
            <span className="rounded-md px-1.5 py-0.5 text-xs font-medium uppercase text-gray-500">
              <SlOptions />
            </span>
          </span>
        </a>
      </div>
    </div>
  );
}

export default LeftNav;
