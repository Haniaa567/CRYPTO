import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import Mapearth from '../assets/8081_earthbump10k.jpg'; // Assuming the texture is in this path

const ShaderSphere = () => {
  const mountRef = useRef(null);

  useEffect(() => {
    // Scene setup
    const scene = new THREE.Scene();

    // Camera setup
    const sizes = { width: window.innerWidth / 2, height: window.innerHeight };
    const camera = new THREE.PerspectiveCamera(30, sizes.width / sizes.height, 1, 1000);
    camera.position.z = 100;
    camera.updateProjectionMatrix();

    // Lighting setup
    const dlight = new THREE.DirectionalLight(0xffffff, 0.8);
    dlight.position.set(100, 2000, 400);
    camera.add(dlight);

    const dlight1 = new THREE.DirectionalLight(0x7982f6, 1);
    dlight1.position.set(-200, 500, 200);
    camera.add(dlight1);

    const ambientlight = new THREE.AmbientLight(0xbbbbbb, 0.3);
    scene.add(ambientlight);

    scene.add(camera);

    // Renderer setup
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(sizes.width, sizes.height);
    renderer.setPixelRatio(window.devicePixelRatio);
    mountRef.current.appendChild(renderer.domElement);

    // Controls setup
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.autoRotate = true;
    controls.autoRotateSpeed = 1.2;
    controls.enableDamping = true;
   // minimum zoom distance
    controls.maxDistance = 100; 
    controls.minDistance = 50; 


    // Texture loader
    const textureLoader = new THREE.TextureLoader();
    const texture = textureLoader.load(Mapearth, () => {
      console.log("Texture loaded successfully");
    }, undefined, (err) => {
      console.error("Error loading texture", err);
    });


    // Sphere geometry and material (Earth)
    const sphereGeometry = new THREE.SphereGeometry(19.5, 35, 35);
    const sphereMaterial = new THREE.MeshBasicMaterial({
      map: texture, 
      color: 0x00ff00, 
      
     
      
   
    });
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    scene.add(sphere);

    // Glow effect (Shadow-like halo)
    const haloGeometry = new THREE.SphereGeometry(20.5, 64, 64); // Slightly larger sphere for halo
    const haloMaterial = new THREE.MeshBasicMaterial({
      color: 0x00ff00, // Glow color
      transparent: true,
      opacity: 0.1, // Very subtle for shadow effect
      side: THREE.BackSide, // Render inside-out for halo effect
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide
    });
    const haloMesh = new THREE.Mesh(haloGeometry, haloMaterial);
    haloMesh.scale.set(1.05, 1.05, 1.05); // Subtle enlargement for shadow glow
    scene.add(haloMesh);

   

    // Animation loop
    const clock = new THREE.Clock();
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };

    animate();

    // Handle window resize
    const handleResize = () => {
      sizes.width = window.innerWidth / 2;
      sizes.height = window.innerHeight;
      camera.aspect = sizes.width / sizes.height;
      camera.updateProjectionMatrix();
      renderer.setSize(sizes.width, sizes.height);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      /*mountRef.current.removeChild(renderer.domElement);*/
    };
  }, []);

  return <div ref={mountRef} style={{
    width: '100%',
    height: '100%',
    position: 'relative',
    overflow: 'hidden',
  }} />;
};

export default ShaderSphere;