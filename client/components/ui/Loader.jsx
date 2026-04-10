"use client";

import { useEffect, useState } from "react";

const messages = [
  "🐹 Hamster is reading your prompt...",
  "🤔 'Hmm... interesting plot...'",
  "🎨 Tiny paws sketching panels...",
  "🤖 Hamster calling AI for backup...",
  "🔥 Adding drama, action & plot twists...",
  "✨ Final touches... hamster nods! 🐹"
];

const Loader = () => {
  const [textIndex, setTextIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTextIndex((prev) => (prev + 1) % messages.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="overlay">
      <div className="content">

        {/* 🐹 EXACT HAMSTER */}
        <div className="wheel-and-hamster">
          <div className="wheel" />
          <div className="hamster">
            <div className="hamster__body">
              <div className="hamster__head">
                <div className="hamster__ear" />
                <div className="hamster__eye" />
                <div className="hamster__nose" />
              </div>
              <div className="hamster__limb hamster__limb--fr" />
              <div className="hamster__limb hamster__limb--fl" />
              <div className="hamster__limb hamster__limb--br" />
              <div className="hamster__limb hamster__limb--bl" />
              <div className="hamster__tail" />
            </div>
          </div>
          <div className="spoke" />
        </div>

        {/* 🔄 Dynamic Text */}
        <p className="loader-text">{messages[textIndex]}</p>
      </div>

      {/* ✅ EXACT CSS (UNCHANGED) */}
      <style jsx>{`
        .overlay {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.9);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 9999;
        }

        .content {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 20px;
        }

        .loader-text {
          color: white;
          font-size: 18px;
          animation: fade 1.5s ease-in-out infinite alternate;
        }

        @keyframes fade {
          from { opacity: 0.5; }
          to { opacity: 1; }
        }

        /* ===== YOUR ORIGINAL HAMSTER CSS (UNCHANGED) ===== */

        .wheel-and-hamster {
          --dur: 0.65s;
          position: relative;
          width: 12em;
          height: 12em;
          font-size: 14px;
        }

        .wheel,
        .hamster,
        .hamster div,
        .spoke {
          position: absolute;
        }

        .wheel,
        .spoke {
          border-radius: 50%;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
        }

        .wheel {
          background: radial-gradient(100% 100% at center,hsla(0,0%,60%,0) 47.8%,hsl(0,0%,60%) 48%);
          z-index: 2;
        }

        .hamster {
          animation: hamster var(--dur) ease-in-out infinite;
          top: 50%;
          left: calc(50% - 3.5em);
          width: 7em;
          height: 3.75em;
          transform: rotate(4deg) translate(-0.8em,1.85em);
          transform-origin: 50% 0;
          z-index: 1;
        }

        .hamster__head {
          animation: hamsterHead var(--dur) ease-in-out infinite;
          background: hsl(30,90%,55%);
          border-radius: 70% 30% 0 100% / 40% 25% 25% 60%;
          box-shadow: 0 -0.25em 0 hsl(30,90%,80%) inset,
            0.75em -1.55em 0 hsl(30,90%,90%) inset;
          top: 0;
          left: -2em;
          width: 2.75em;
          height: 2.5em;
          transform-origin: 100% 50%;
        }

        .hamster__ear {
          animation: hamsterEar var(--dur) ease-in-out infinite;
          background: hsl(0,90%,85%);
          border-radius: 50%;
          box-shadow: -0.25em 0 hsl(30,90%,55%) inset;
          top: -0.25em;
          right: -0.25em;
          width: 0.75em;
          height: 0.75em;
          transform-origin: 50% 75%;
        }

        .hamster__eye {
          animation: hamsterEye var(--dur) linear infinite;
          background-color: black;
          border-radius: 50%;
          top: 0.375em;
          left: 1.25em;
          width: 0.5em;
          height: 0.5em;
        }

        .hamster__nose {
          background: hsl(0,90%,75%);
          border-radius: 35% 65% 85% 15% / 70% 50% 50% 30%;
          top: 0.75em;
          left: 0;
          width: 0.2em;
          height: 0.25em;
        }

        .hamster__body {
          animation: hamsterBody var(--dur) ease-in-out infinite;
          background: hsl(30,90%,90%);
          border-radius: 50% 30% 50% 30% / 15% 60% 40% 40%;
          box-shadow: 0.1em 0.75em 0 hsl(30,90%,55%) inset,
            0.15em -0.5em 0 hsl(30,90%,80%) inset;
          top: 0.25em;
          left: 2em;
          width: 4.5em;
          height: 3em;
          transform-origin: 17% 50%;
        }

        .hamster__limb--fr,
        .hamster__limb--fl {
          clip-path: polygon(0 0,100% 0,70% 80%,60% 100%,0% 100%,40% 80%);
          top: 2em;
          left: 0.5em;
          width: 1em;
          height: 1.5em;
          transform-origin: 50% 0;
        }

        .hamster__limb--fr {
          animation: hamsterFRLimb var(--dur) linear infinite;
          background: linear-gradient(hsl(30,90%,80%) 80%,hsl(0,90%,75%) 80%);
        }

        .hamster__limb--fl {
          animation: hamsterFLLimb var(--dur) linear infinite;
          background: linear-gradient(hsl(30,90%,90%) 80%,hsl(0,90%,85%) 80%);
        }

        .hamster__limb--br,
.hamster__limb--bl {
  border-radius: 0.75em 0.75em 0 0;
  clip-path: polygon(
    0 0,
    100% 0,
    100% 30%,
    70% 90%,
    70% 100%,
    30% 100%,
    40% 90%,
    0% 30%
  );
  top: 1em;
  left: 2.8em;
  width: 1.5em;
  height: 2.5em;
  transform-origin: 50% 30%;
}

        .hamster__limb--br {
  animation: hamsterBRLimb var(--dur) linear infinite;
  background: linear-gradient(
    hsl(30,90%,80%) 90%,
    hsl(0,90%,75%) 90%
  );
  transform: rotate(-25deg) translateZ(-1px);
}

.hamster__limb--bl {
  animation: hamsterBLLimb var(--dur) linear infinite;
  background: linear-gradient(
    hsl(30,90%,90%) 90%,
    hsl(0,90%,85%) 90%
  );
  transform: rotate(-25deg);
}
        .hamster__tail {
          animation: hamsterTail var(--dur) linear infinite;
          background: hsl(0,90%,85%);
          border-radius: 0.25em 50% 50% 0.25em;
          top: 1.5em;
          right: -0.5em;
          width: 1em;
          height: 0.5em;
        }
.spoke {
  animation: spoke var(--dur) linear infinite;

  background: linear-gradient(
    transparent 46%,
    #ccc 47%,
    #fff 50%,
    #ccc 53%,
    transparent 54%
  );

  border-radius: 50%;
}

        @keyframes hamster { 50% { transform: rotate(0) translate(-0.8em,1.85em); } }
        @keyframes hamsterHead { 50% { transform: rotate(8deg); } }
        @keyframes hamsterEye { 95% { transform: scaleY(0); } }
        @keyframes hamsterEar { 50% { transform: rotate(12deg); } }
        @keyframes hamsterBody { 50% { transform: rotate(-2deg); } }
        @keyframes hamsterFRLimb { 50% { transform: rotate(-30deg); } }
        @keyframes hamsterFLLimb { 50% { transform: rotate(50deg); } }
        @keyframes hamsterBRLimb { 50% { transform: rotate(20deg); } }
        @keyframes hamsterBLLimb { 50% { transform: rotate(-60deg); } }
        @keyframes hamsterTail { 50% { transform: rotate(10deg); } }
        @keyframes spoke { to { transform: rotate(-360deg); } }

      `}</style>
    </div>
  );
};

export default Loader;