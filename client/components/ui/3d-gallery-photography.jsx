// "use client";

// import { useRef, useMemo } from "react";
// import { Canvas, useFrame } from "@react-three/fiber";
// import { useTexture } from "@react-three/drei";
// import * as THREE from "three";

// function ImagePlane({ url, position, scale = [2.4, 3.2, 1] }) {
//   const texture = useTexture(url);
//   const meshRef = useRef();

//   useFrame((state) => {
//     if (meshRef.current) {
//       meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 0.5 + position[0]) * 0.15;
//     }
//   });

//   return (
//     <mesh ref={meshRef} position={position}>
//       <planeGeometry args={[scale[0], scale[1]]} />
//       <meshBasicMaterial map={texture} toneMapped={false} />
//     </mesh>
//   );
// }

// function GalleryScene({ images }) {
//   const groupRef = useRef();

//   const positions = useMemo(() => {
//     const cols = images.length;
//     return images.map((_, i) => {
//       const x = (i - (cols - 1) / 2) * 3;
//       const y = 0;
//       const z = -2 + Math.sin(i * 0.8) * 1.5;
//       return [x, y, z];
//     });
//   }, [images]);

//   useFrame((state) => {
//     if (groupRef.current) {
//       groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.15) * 0.08;
//     }
//   });

//   return (
//     <group ref={groupRef}>
//       {images.map((img, i) => (
//         <ImagePlane key={i} url={img} position={positions[i]} />
//       ))}
//     </group>
//   );
// }

// export default function InfiniteGallery({ images }) {
//   return (
//     <div className="w-full h-full">
//       <Canvas
//         camera={{ position: [0, 0, 8], fov: 50 }}
//         gl={{ antialias: true, alpha: true }}
//         style={{ background: "transparent" }}
//       >
//         <ambientLight intensity={1} />
//         <GalleryScene images={images} />
//       </Canvas>
//     </div>
//   );
// }


"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { useTexture } from "@react-three/drei";

function ImagePlane({ url, position, scale = [2.4, 3.2, 1] }) {
  const texture = useTexture(url);
  const meshRef = useRef();

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.y =
        position[1] +
        Math.sin(state.clock.elapsedTime * 0.5 + position[0]) * 0.15;
    }
  });

  return (
    <mesh ref={meshRef} position={position}>
      <planeGeometry args={[scale[0], scale[1]]} />
      <meshBasicMaterial map={texture} toneMapped={false} />
    </mesh>
  );
}

function GalleryScene({ images }) {
  const groupRef = useRef();

  const positions = useMemo(() => {
    const cols = images.length;
    return images.map((_, i) => {
      const x = (i - (cols - 1) / 2) * 3;
      const y = 0;
      const z = -2 + Math.sin(i * 0.8) * 1.5;
      return [x, y, z];
    });
  }, [images]);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y =
        Math.sin(state.clock.elapsedTime * 0.15) * 0.08;
    }
  });

  return (
    <group ref={groupRef}>
      {images.map((img, i) => (
        <ImagePlane key={i} url={img} position={positions[i]} />
      ))}
    </group>
  );
}

export default function InfiniteGallery3D({ images }) {
  return (
    <Canvas
      camera={{ position: [0, 0, 8], fov: 50 }}
      gl={{ antialias: true, alpha: true }}
      style={{ background: "transparent", width: "100%", height: "100%" }}
    >
      <ambientLight intensity={1} />
      <GalleryScene images={images} />
    </Canvas>
  );
}