import React, { useContext } from "react";
import { ContextApp } from "../utils/Context";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

function Chat() {
  const { message, msgEnd, isLoading } = useContext(ContextApp);
  return (
    <div className="w-full h-[85%] flex items-center justify-center overflow-hidden overflow-y-auto px-2 py-1 scroll ">
      <div className="w-full lg:w-4/5 flex flex-col h-full items-start justify-start ">
        {message?.map((msg, i) => (
          <div
            key={i}
            className={`flex items-start gap-2 lg:gap-5 my-2 p-3 rounded-md max-w-full lg:max-w-[90%]  ${
              msg.isBot
                ? "bg-gray-800/80 text-left self-start"
                : "bg-blue-600 text-left self-end"
            }`}
          >
            {msg.isBot && (
              <a
                href="https://www.youtube.com/@SwAt1563"
                target="_blank"
                rel="noopener noreferrer"
              >
                <img
                  src="/icon.png"
                  alt="bot"
                  className="w-10 h-10 rounded-full object-cover self-start"
                />
              </a>
            )}
            <Markdown
              className="text-white text-[15px] max-w-full !whitespace-pre-wrap overflow-auto"
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight]}
            >
              {msg?.text}
            </Markdown>
          </div>
        ))}

        {/* Loading message */}
        {isLoading && (
          <div className="flex items-start justify-center gap-2 lg:gap-5 my-2 bg-gray-700 p-3 rounded-md">
            <a
              href="https://www.youtube.com/@SwAt1563"
              target="_blank"
              rel="noopener noreferrer"
            >
              <img
                src="/icon.png"
                alt="bot"
                className="w-10 h-10 rounded-full object-cover"
              />
            </a>
            <p className="text-white text-[15px] flex items-center">
              <span className="typing-dots">.</span>
              <span className="typing-dots">.</span>
              <span className="typing-dots">.</span>
            </p>
          </div>
        )}

        <div ref={msgEnd} />
      </div>
    </div>
  );
}

export default Chat;
