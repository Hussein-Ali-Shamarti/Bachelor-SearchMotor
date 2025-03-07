// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore"; // Importer Firestore
import { getAuth } from "firebase/auth"; // Importer Auth
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA_TT2Vwj6DZBk-dcwZrGFzhzQLtn-J2CU",
  authDomain: "hybridsearchai.firebaseapp.com",
  projectId: "hybridsearchai",
  storageBucket: "hybridsearchai.firebasestorage.app",
  messagingSenderId: "183726086411",
  appId: "1:183726086411:web:e9c0b0b9cea5201efcaa0e",
  measurementId: "G-23MT3N6XTM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app); // Initialiser Firestore
const auth = getAuth(app); // Initialiser Authentication

export { app, auth, db }; // Eksporter Auth slik at vi kan bruke den i andre filer