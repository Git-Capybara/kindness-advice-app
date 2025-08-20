console.log("react app starting...");
import React, { useState, useEffect, useCallback } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, signInWithCustomToken, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, collection, addDoc, query, onSnapshot, serverTimestamp, doc, getDoc, setDoc, updateDoc, increment } from 'firebase/firestore';

// Global variables provided by the Canvas environment
// The appId variable below is used for data paths in Firestore to ensure persistence.
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
const firebaseConfig = {

  apiKey: "AIzaSyBLYemOXieL4fTbEaMlO3vW4ZLzp0GDY8s",

  authDomain: "kindness-advice-column.firebaseapp.com",

  projectId: "kindness-advice-column",

  storageBucket: "kindness-advice-column.firebasestorage.app",

  messagingSenderId: "541838051756",

  appId: "1:541838051755:web:3b074a5f7bee7454a46aee",

  measurementId: "G-SH6M5WL48K"

};

const initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

/**
* Component for the input field and button to post a reply to a specific suggestion.
* Manages its own local state for the reply text and posting status.
*/

function ReplyInput({ problemId, responseId, handlePostReply, userId }) {
 const [replyText, setReplyText] = useState('');
 const [replyMessage, setReplyMessage] = useState('');
 const [isReplying, setIsReplying] = useState(false);


 const onPostReply = async () => {
   // Pass local state setters to the parent's handlePostReply for message and loading management
   await handlePostReply(problemId, responseId, replyText, setReplyMessage, setIsReplying);
   setReplyText(''); // Clear input after attempting to post
 };


 return (
   <div className="mt-3">
     <textarea
       className="w-full p-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-blue-400 focus:border-transparent transition duration-200 ease-in-out resize-y text-sm min-h-[50px]"
       placeholder="Reply kindly to this suggestion..."
       value={replyText}
       onChange={(e) => setReplyText(e.target.value)}
       rows="2"
       disabled={isReplying}
     ></textarea>
     <button
       onClick={onPostReply}
       className={`w-full mt-2 py-1.5 px-3 rounded-lg text-white font-semibold text-sm shadow-sm transition duration-300 ease-in-out
         ${isReplying ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'}`}
       disabled={isReplying}
     >
       {isReplying ? 'Replying...' : 'Post Reply'}
     </button>
     {replyMessage && (
       <p className={`mt-1 text-center text-xs ${replyMessage.includes('successfully') ? 'text-green-600' : 'text-red-600'}`}>
         {replyMessage}
       </p>
     )}
   </div>
 );
}




/**
* Component to display a single problem and its responses.
* It also handles posting new responses for this problem and replies to suggestions.
*/
function ProblemItem({ problem, db, userId, aiCheckFunction, updateKindnessCounter }) {
 const [responses, setResponses] = useState([]);
 const [newResponseText, setNewResponseText] = useState('');
 const [isResponding, setIsResponding] = useState(false);
 const [responseMessage, setResponseMessage] = useState('');
 const [repliesMap, setRepliesMap] = useState({}); // To store replies for each responseId


 // Fetch responses for this problem
 useEffect(() => {
   if (!db || !problem.id) return;


   const responsesCollectionRef = collection(db, `artifacts/${appId}/public/data/problems/${problem.id}/responses`);
   // Note: Firestore orderBy can cause issues without indexes. Sorting in memory.
   const q = query(responsesCollectionRef);


   const unsubscribe = onSnapshot(q, (snapshot) => {
     const fetchedResponses = snapshot.docs.map(doc => ({
       id: doc.id,
       ...doc.data()
     }));
     // Sort responses by timestamp in ascending order
     fetchedResponses.sort((a, b) => (a.timestamp?.toDate() || 0) - (b.timestamp?.toDate() || 0));
     setResponses(fetchedResponses);
   }, (error) => {
     console.error(`Error fetching responses for problem ${problem.id}:`, error);
   });


   return () => unsubscribe();
 }, [db, problem.id]);


 // Effect to fetch replies for each response
 useEffect(() => {
   if (!db || responses.length === 0) return;


   const unsubscribes = [];
   responses.forEach(response => {
     const repliesCollectionRef = collection(db, `artifacts/${appId}/public/data/problems/${problem.id}/responses/${response.id}/replies`);
     const q = query(repliesCollectionRef);


     const unsubscribe = onSnapshot(q, (snapshot) => {
       const fetchedReplies = snapshot.docs.map(doc => ({
         id: doc.id,
         ...doc.data()
       }));
       fetchedReplies.sort((a, b) => (a.timestamp?.toDate() || 0) - (b.timestamp?.toDate() || 0));
       setRepliesMap(prev => ({
         ...prev,
         [response.id]: fetchedReplies
       }));
     }, (error) => {
       console.error(`Error fetching replies for response ${response.id}:`, error);
     });
     unsubscribes.push(unsubscribe);
   });


   return () => unsubscribes.forEach(unsub => unsub());
 }, [db, problem.id, responses]); // Depend on responses to re-fetch replies if responses change




 const handlePostResponse = async () => {
   if (!newResponseText.trim()) {
     setResponseMessage('Please enter your suggestion.');
     return;
   }
   if (!db || !userId) {
     setResponseMessage('Authentication not ready. Please wait.');
     return;
   }


   setIsResponding(true);
   setResponseMessage('Checking suggestion with AI...');


   try {
     const { isKind, reason } = await aiCheckFunction(newResponseText, false); // Pass false to indicate not a problem


     if (isKind) {
       const responsesCollectionRef = collection(db, `artifacts/${appId}/public/data/problems/${problem.id}/responses`);
       await addDoc(responsesCollectionRef, {
         text: newResponseText,
         timestamp: serverTimestamp(),
         userId: userId, // Store user ID for responses
       });
       setNewResponseText('');
       setResponseMessage('Suggestion posted successfully!');


       // Increment the global kindness counter
       await updateKindnessCounter(); // Call the passed-down function


     } else {
       setResponseMessage(`Suggestion not posted: ${reason || 'It was not deemed kind or appropriate.'}`);
     }
   } catch (error) {
     console.error("Error during AI check or posting response:", error);
     setResponseMessage('An error occurred during AI check or posting. Please try again.');
   } finally {
     setIsResponding(false);
   }
 };


 const handlePostReply = useCallback(async (currentProblemId, responseId, replyText, setReplyMessage, setIsReplying) => {
   if (!replyText.trim()) {
     setReplyMessage('Please enter your reply.');
     return;
   }
   if (!db || !userId) {
     setReplyMessage('Authentication not ready. Please wait.');
     return;
   }


   setIsReplying(true);
   setReplyMessage('Checking reply with AI...');


   try {
     const { isKind, reason } = await aiCheckFunction(replyText, false); // Still checking for kindness


     if (isKind) {
       const repliesCollectionRef = collection(db, `artifacts/${appId}/public/data/problems/${currentProblemId}/responses/${responseId}/replies`);
       await addDoc(repliesCollectionRef, {
         text: replyText,
         timestamp: serverTimestamp(),
         userId: userId,
       });
       setReplyMessage('Reply posted successfully!');
       await updateKindnessCounter(); // Increment global kindness for replies too
     } else {
       setReplyMessage(`Reply not posted: ${reason || 'It was not deemed kind or appropriate.'}`);
     }
   } catch (error) {
     console.error("Error during AI check or posting reply:", error);
     setReplyMessage('An error occurred during AI check or posting. Please try again.');
   } finally {
     setIsReplying(false);
   }
 }, [db, userId, aiCheckFunction, updateKindnessCounter]); // Dependencies for useCallback




 // Determine who posted the problem
 const problemPoster = problem.isSample ? problem.userId : 'Anonymous User';


 return (
   <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 mb-6">
     <p className="text-gray-800 text-lg font-semibold mb-3">{problem.text}</p>
     <div className="flex justify-between items-center text-sm text-gray-500 mb-4 border-b pb-2 border-gray-100">
       <span>Problem by: <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded-md break-all">{problemPoster}</span></span>
       {problem.timestamp && (
         <span>{new Date(problem.timestamp.toDate()).toLocaleString()}</span>
       )}
     </div>


     <h3 className="text-md font-bold text-gray-700 mb-3">Suggestions:</h3>
     {responses.length === 0 ? (
       <p className="text-gray-500 text-sm mb-4">No suggestions yet. Be the first to help!</p>
     ) : (
       <div className="space-y-4 mb-4"> {/* Increased space for better visual separation */}
         {responses.map((response) => (
           <div key={response.id} className="bg-gray-50 p-3 rounded-md border border-gray-100">
             <p className="text-gray-700 text-sm mb-1">{response.text}</p>
             <div className="flex justify-between items-center text-xs text-gray-400">
               <span>By: <span className="font-mono break-all">{response.userId}</span></span>
               {response.timestamp && (
                 <span>{new Date(response.timestamp.toDate()).toLocaleString()}</span>
               )}
             </div>


             {/* Replies section */}
             <div className="mt-3 ml-4 border-l-2 border-gray-200 pl-4"> {/* Visual line for replies */}
               <h4 className="text-sm font-semibold text-gray-600 mb-2">Replies:</h4>
               {repliesMap[response.id]?.length > 0 ? (
                 <div className="space-y-2">
                   {repliesMap[response.id].map(reply => (
                     <div key={reply.id} className="bg-gray-100 p-2 rounded-md border border-gray-200 text-sm">
                       <p className="text-gray-700 mb-1">{reply.text}</p>
                       <div className="flex justify-between items-center text-xs text-gray-500">
                         <span>By: <span className="font-mono break-all">{reply.userId}</span></span>
                         {reply.timestamp && (
                           <span>{new Date(reply.timestamp.toDate()).toLocaleString()}</span>
                         )}
                       </div>
                     </div>
                   ))}
                 </div>
               ) : (
                 <p className="text-gray-500 text-xs">No replies yet.</p>
               )}


               {/* Reply input for this specific response */}
               <ReplyInput
                 problemId={problem.id}
                 responseId={response.id}
                 handlePostReply={handlePostReply}
                 userId={userId}
               />
             </div>
           </div>
         ))}
       </div>
     )}


     <div className="mt-4 pt-4 border-t border-gray-100">
       <textarea
         className="w-full p-3 border border-gray-300 rounded-lg focus:ring-1 focus:ring-indigo-400 focus:border-transparent transition duration-200 ease-in-out resize-y min-h-[70px]"
         placeholder="Type your kind suggestion here..."
         value={newResponseText}
         onChange={(e) => setNewResponseText(e.target.value)}
         rows="3"
         disabled={isResponding}
       ></textarea>
       <button
         onClick={handlePostResponse}
         className={`w-full mt-3 py-2 px-4 rounded-lg text-white font-semibold shadow-sm transition duration-300 ease-in-out
           ${isResponding ? 'bg-green-400 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2'}`}
         disabled={isResponding}
       >
         {isResponding ? 'Suggesting...' : 'Post Suggestion'}
       </button>
       {responseMessage && (
         <p className={`mt-2 text-center text-xs ${responseMessage.includes('successfully') ? 'text-green-600' : 'text-red-600'}`}>
           {responseMessage}
         </p>
       )}
     </div>
   </div>
 );
}


function ApplicationStuff() {
 const [db, setDb] = useState(null);
 const [auth, setAuth] = useState(null);
 const [userId, setUserId] = useState(null);
 const [isAuthReady, setIsAuthReady] = useState(false);
 const [problemText, setProblemText] = useState('');
 const [problems, setProblems] = useState([]);
 const [loading, setLoading] = useState(true);
 const [aiCheckMessage, setAiCheckMessage] = useState('');
 const [isPostingProblem, setIsPostingProblem] = useState(false);


 // State for private AI advice feature
 const [privateProblemText, setPrivateProblemText] = useState('');
 const [aiGeneratedAdvice, setAiGeneratedAdvice] = useState('');
 const [isGeneratingAdvice, setIsGeneratingAdvice] = useState(false);
 const [privateAdviceMessage, setPrivateAdviceMessage] = useState('');


 // New state for the kindness counter
 const [kindnessCount, setKindnessCount] = useState(0);


 // States to manage the celebratory feature
 const [showCelebration, setShowCelebration] = useState(false);


 // State to control visibility of "About this app" section
 const [showAboutSection, setShowAboutSection] = useState(true);




 // Initialize Firebase and set up authentication listener
 useEffect(() => {
   // Moved console.log for isAuthReady here
   console.log("isAuthReady = ", isAuthReady); 

   try {
     const app = initializeApp(firebaseConfig); // Use firebaseConfig from Canvas environment
     const firestore = getFirestore(app);
     const firebaseAuth = getAuth(app);


     setDb(firestore);
     setAuth(firebaseAuth);


     const unsubscribe = onAuthStateChanged(firebaseAuth, async (user) => {
       if (user) {
         setUserId(user.uid);
       } else {
         try {
           if (initialAuthToken) {
             await signInWithCustomToken(firebaseAuth, initialAuthToken);
           } else {
             await signInAnonymously(firebaseAuth);
           }
         } catch (error) {
           console.error("Error signing in:", error);
           setUserId(crypto.randomUUID()); // Fallback to a random UUID
         }
       }
       setIsAuthReady(true);
     });


     return () => unsubscribe();
   } catch (error) {
     console.error("Failed to initialize Firebase:", error);
     setLoading(false);
   }
 }, []);


 // AI Kindness Check function (reusable for problems and responses)
 const aiCheckFunction = useCallback(async (textToCheck, isProblem = true) => {
   const promptType = isProblem ? "problem description" : "suggestion";
   const prompt = `Evaluate the following ${promptType} for kindness, politeness, and appropriateness. It should not contain any offensive, hateful, or derogatory language. Respond with a JSON object containing "isKind" (boolean) and "reason" (string, explaining why if not kind). Text: "${textToCheck}"`;


   let chatHistory = [];
   chatHistory.push({ role: "user", parts: [{ text: prompt }] });


   const payload = {
     contents: chatHistory,
     generationConfig: {
       responseMimeType: "application/json",
       responseSchema: {
         type: "OBJECT",
         properties: {
           "isKind": { "type": "BOOLEAN" },
           "reason": { "type": "STRING" }
         },
         propertyOrdering: ["isKind", "reason"]
       }
     }
   };


   const apiKey = ""; // Canvas will provide this at runtime
   const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;


   let aiResponse;
   let retries = 0;
   const maxRetries = 5;
   const baseDelay = 1000; // 1 second


   while (retries < maxRetries) {
     try {
       const response = await fetch(apiUrl, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(payload)
       });


       if (!response.ok) {
         if (response.status === 429) { // Too Many Requests
           const delay = baseDelay * Math.pow(2, retries);
           console.warn(`Rate limit hit. Retrying in ${delay / 1000}s...`);
           await new Promise(resolve => setTimeout(resolve, delay));
           retries++;
           continue;
         } else {
           throw new Error(`API request failed with status ${response.status}`);
         }
       }


       aiResponse = await response.json();
       break; // Success, exit loop
     } catch (error) {
       console.error("Error during AI fetch attempt:", error);
       if (retries === maxRetries - 1) throw error;
       const delay = baseDelay * Math.pow(2, retries);
       console.warn(`Fetch failed. Retrying in ${delay / 1000}s...`);
       await new Promise(resolve => setTimeout(resolve, delay));
       retries++;
     }
   }


   const aiResultText = aiResponse?.candidates?.[0]?.content?.parts?.[0]?.text;
   if (!aiResultText) {
     throw new Error("AI response was empty or malformed.");
   }


   return JSON.parse(aiResultText);
 }, []);


 // AI Advice Generation function (for private advice)
 const generateAdviceFromAI = useCallback(async (problemDescription) => {
   const prompt = `You are a helpful and kind advice assistant. Provide a concise, empathetic, and constructive suggestion for the following problem. Focus on positive and actionable steps.
   Problem: "${problemDescription}"
   Suggestion:`;


   let chatHistory = [];
   chatHistory.push({ role: "user", parts: [{ text: prompt }] });


   const payload = {
     contents: chatHistory,
   };


   const apiKey = ""; // Canvas will provide this at runtime
   const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;


   let aiResponse;
   let retries = 0;
   const maxRetries = 5;
   const baseDelay = 1000; // 1 second


   while (retries < maxRetries) {
     try {
       const response = await fetch(apiUrl, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify(payload)
       });


       if (!response.ok) {
         if (response.status === 429) { // Too Many Requests
           const delay = baseDelay * Math.pow(2, retries);
           console.warn(`Rate limit hit. Retrying in ${delay / 1000}s...`);
           await new Promise(resolve => setTimeout(resolve, delay));
           retries++;
           continue;
         } else {
           throw new Error(`API request failed with status ${response.status}`);
         }
       }


       aiResponse = await response.json();
       break; // Success, exit loop
     } catch (error) {
       console.error("Error during AI fetch attempt:", error);
       if (retries === maxRetries - 1) throw error;
       const delay = baseDelay * Math.pow(2, retries);
       console.warn(`Fetch failed. Retrying in ${delay / 1000}s...`);
       await new Promise(resolve => setTimeout(resolve, delay));
       retries++;
     }
   }


   const aiResultText = aiResponse?.candidates?.[0]?.content?.parts?.[0]?.text;
   if (!aiResultText) {
     throw new Error("AI response was empty or malformed.");
   }


   return aiResultText;
 }, []);


 // Sample problems to be seeded into Firestore
 const initialSampleProblems = [
   {
     id: 'sample_problem_1',
     text: "I'm feeling overwhelmed with my workload and struggling to find time for myself. Any advice on managing stress and finding balance?",
     userId: 'AI Helper', // This userId is for internal tracking/display for samples
     isSample: true,
     sampleResponse: {
       text: "It sounds like you're juggling a lot! Try setting small, achievable goals each day and block out short periods for self-care, even just 15 minutes. Remember, it's okay to say no to new commitments when you're feeling stretched.",
       userId: 'Community Supporter',
     }
   },
   {
     id: 'sample_problem_2',
     text: "I had a disagreement with a close friend, and now things feel awkward. How can I approach them to resolve this kindly?",
     userId: 'AI Helper',
     isSample: true,
   },
   {
     id: 'sample_problem_3',
     text: "I'm trying to start a new healthy habit, but I keep losing motivation after a few days. What are some tips to stay consistent?",
     userId: 'AI Helper',
     isSample: true,
   },
 ];


 // Effect to seed sample problems and responses into Firestore
 useEffect(() => {
   const seedSampleData = async () => {
     if (!db || !isAuthReady) return;


     const problemsCollectionRef = collection(db, `artifacts/${appId}/public/data/problems`);


     for (const sample of initialSampleProblems) {
       const problemDocRef = doc(problemsCollectionRef, sample.id);
       const problemDocSnap = await getDoc(problemDocRef);


       if (!problemDocSnap.exists()) {
         console.log(`Seeding sample problem: ${sample.text}`);
         await setDoc(problemDocRef, {
           text: sample.text,
           userId: sample.userId, // Stored, but not displayed for user-posted problems
           timestamp: serverTimestamp(),
           isSample: true, // Mark as sample for display logic
         });


         // Add sample response if specified
         if (sample.sampleResponse) {
           const responsesCollectionRef = collection(problemDocRef, 'responses');
           await addDoc(responsesCollectionRef, {
             text: sample.sampleResponse.text,
             userId: sample.sampleResponse.userId,
             timestamp: serverTimestamp(),
           });
         }
       }
     }
   };


   seedSampleData();
 }, [db, isAuthReady]); // Depend on db and isAuthReady


 // Fetch problems from Firestore once auth is ready
 useEffect(() => {
   if (db && isAuthReady) {
     setLoading(true);
     const problemsCollectionRef = collection(db, `artifacts/${appId}/public/data/problems`);
     const q = query(problemsCollectionRef);


     const unsubscribe = onSnapshot(q, (snapshot) => {
       const fetchedProblems = snapshot.docs.map(doc => ({
         id: doc.id,
         ...doc.data()
       }));
       fetchedProblems.sort((a, b) => (b.timestamp?.toDate() || 0) - (a.timestamp?.toDate() || 0));
       setProblems(fetchedProblems);
       setLoading(false);
     }, (error) => {
       console.error("Error fetching problems:", error);
       setLoading(false);
     });


     return () => unsubscribe();
   }
 }, [db, isAuthReady]);


 // Fetch the kindness counter from Firestore
 useEffect(() => {
   if (!db || !isAuthReady) return;


   const kindnessStatsDocRef = doc(db, `artifacts/${appId}/public/data/app_metadata/kindness_stats`);

   console.log("#### useEffect, before calling onSnapshot kindnessStatsDocRef");
   console.log("#### uid = ", userId);
   const unsubscribe = onSnapshot(kindnessStatsDocRef, (docSnap) => { // Corrected variable name here
     if (docSnap.exists()) {
       console.log("docSnap.exists() == true");
       setKindnessCount(docSnap.data().totalKindResponses || 0);
     } else {
      console.log("docSnap.exists() == false");
       // If the document doesn't exist yet, it means no kind responses have been posted.
       setKindnessCount(0);
     }
   }, (error: any) => {
     console.error("Error fetching kindness counter:", error);
   });


   return () => unsubscribe();
 }, [db, isAuthReady]);


 // Function to update the global kindness counter
 const updateKindnessCounter = useCallback(async () => {
   if (!db) return;


   const kindnessStatsDocRef = doc(db, `artifacts/${appId}/public/data/app_metadata/kindness_stats`);


   try {
     // Use setDoc with merge: true to create the document if it doesn't exist,
     // or update it if it does. This ensures the counter starts at 0.
     await setDoc(kindnessStatsDocRef, {
       totalKindResponses: increment(1) // Atomically increment by 1
     }, { merge: true }); // Important: merge ensures existing fields aren't overwritten
     console.log("Kindness counter incremented!");
     // console.log("$$$$$",db); // Removed this console.log
   } catch (error) {
     console.error("Error incrementing kindness counter:", error);
   }
 }, [db]); // Dependency: db


 // Effect to handle the celebratory feature
 useEffect(() => {
   // Check if the kindness count is a multiple of 10 (and not 0)
   if (kindnessCount > 0 && kindnessCount % 10 === 0) {
     // Show the celebration
     setShowCelebration(true);


     // Hide it after 15 seconds
     const timer = setTimeout(() => {
       setShowCelebration(false);
     }, 15000); // 15 seconds


     // Cleanup function to clear the timeout if the component unmounts
     return () => clearTimeout(timer);
   }
 }, [kindnessCount]); // Rerun this effect whenever the kindness count changes


 const handlePostProblem = async () => {
   if (!problemText.trim()) {
     setAiCheckMessage('Please describe your problem.');
     return;
   }
   if (!db || !userId) {
     setAiCheckMessage('Authentication not ready. Please wait.');
     return;
   }


   setIsPostingProblem(true);
   setAiCheckMessage('Posting problem...'); // Update message to reflect no AI check


   try {
     const problemsCollectionRef = collection(db, `artifacts/${appId}/public/data/problems`);
     await addDoc(problemsCollectionRef, {
       text: problemText,
       timestamp: serverTimestamp(),
       userId: userId, // Store userId internally, but display as anonymous
       isSample: false, // Explicitly mark as not a sample
     });
     setProblemText('');
     setAiCheckMessage('Problem posted successfully!');
   } catch (error) {
     console.error("Error posting problem:", error);
     setAiCheckMessage('An error occurred during posting. Please try again.');
   } finally {
     setIsPostingProblem(false);
   }
 };


 const handleAskAIForPrivateAdvice = async () => {
   if (!privateProblemText.trim()) {
     setPrivateAdviceMessage('Please describe your problem to the AI.');
     return;
   }


   setIsGeneratingAdvice(true);
   setPrivateAdviceMessage('AI is generating advice...');
   setAiGeneratedAdvice(''); // Clear previous advice


   try {
     const advice = await generateAdviceFromAI(privateProblemText);
     setAiGeneratedAdvice(advice);
     setPrivateAdviceMessage('Advice generated!');
   } catch (error) {
     console.error("Error generating AI advice:", error);
     setPrivateAdviceMessage('An error occurred while getting AI advice. Please try again.');
   } finally {
     setIsGeneratingAdvice(false);
   }
 };


 if (!isAuthReady || loading) {
   return (
     <div className="flex items-center justify-center min-h-screen bg-gray-100">
       <div className="text-lg font-semibold text-gray-700">Loading application...</div>
     </div>
   );
 }


 return (
   <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4 sm:p-6 relative">
     {/* Container for the celebration (emoji and message), positioned absolutely at the top-right */}
     {showCelebration && (
       <div className="fixed top-4 right-4 z-50 flex items-center bg-white p-4 rounded-full shadow-lg border border-purple-200 animate-slideIn">
         <span className="text-5xl mr-4">😊</span> {/* Smiling face emoji */}
         <div className="text-purple-700 font-bold text-lg">
           <p>CONGRATULATIONS!</p>
           <p>10 new kind suggestions have been posted!</p>
         </div>
       </div>
     )}


     <div className="w-full max-w-2xl bg-white rounded-lg shadow-xl p-6 sm:p-8">
       <div className="flex items-center justify-center mb-6">
         <h1 className="text-3xl sm:text-4xl font-extrabold text-purple-700 text-center">
           Kindness Advice Column
         </h1>
       </div>


       {/* Display the kindness counter */}
       <p className="text-center text-gray-600 mb-2">
         Total Kind Suggestions Posted: <span className="font-bold text-purple-600 text-xl">{kindnessCount}</span>
       </p>
       <p className="text-center text-gray-600 mb-8">
         Post your problems here and receive kind suggestions from the community, or ask our AI for private advice!
       </p>


       {/* Debug statement for appId */}
       <p className="text-center text-gray-500 mb-4">
         App ID: <span className="font-mono text-xs bg-gray-200 px-2 py-1 rounded-md break-all">{appId}</span>
       </p>


       {/* About This App Section */}
       {showAboutSection && (
         <div className="mb-8 p-4 bg-gray-50 rounded-lg border border-gray-200 relative">
           <button
             onClick={() => setShowAboutSection(false)}
             className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 transition-colors z-10 p-1" // Added p-1 for larger clickable area
             aria-label="Close about section"
           >
             <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
             </svg>
           </button>
           <h2 className="text-xl font-bold text-gray-800 mb-4">About This App</h2>
           <p className="text-gray-700 mb-3">
             Welcome to the Kindness Advice Column! This app is designed to be a supportive and positive space where you can seek and offer kind advice.
           </p>
           <ul className="list-disc list-inside text-gray-700 space-y-2">
             <li>
               Post Your Problem (Public with Anonymous Name): Share your challenges with the community in the purple section. Your identity will remain anonymous to other users.
             </li>
             <li>
               Ask AI for Private Advice: If you prefer a private consultation, use the blue section to get a kind and constructive suggestion from our AI assistant. This advice is just for you and isn't shared publicly. If you choose to use this feature to ask your question, your problem and the solution the AI gives will not be posted.
             </li>
             <li>
               Offer Kind Suggestions: Browse problems posted by others in the "Community Problems & Suggestions" section. You can offer your helpful advice, and every kind suggestion you post will contribute to the global kindness counter! All suggestions are checked by AI to ensure they are kind and helpful.
             </li>
             <li>
               Reply to Suggestions: Engage deeper by replying directly to existing suggestions. These replies are also checked for kindness and visually connected to the original suggestion. Feel free to post how someone's suggestion changed your day, or add on to their idea with this feature.
             </li>
             <li>
               Kindness Milestones: Keep an eye on the "Total Kind Suggestions Posted" counter! Every time the community reaches a milestone of 10 kind suggestions, a special congratulatory message will appear to celebrate the kindness of the community.
             </li>
           </ul>
           <p className="text-gray-700 mt-3">
             Our goal is to create a kind and encouraging environment for everyone. Thank you for being a part of this awesome community!
           </p>
         </div>
       )}


       <div className="mb-8 p-4 bg-purple-50 rounded-lg border border-purple-200">
         <h2 className="text-xl font-bold text-purple-800 mb-4">Post Your Problem (Public with Anonymous Name)</h2>
         <textarea
           className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200 ease-in-out resize-y min-h-[100px]"
           placeholder="Describe your problem or situation here for the community to see..."
           value={problemText}
           onChange={(e) => setProblemText(e.target.value)}
           rows="4"
           disabled={isPostingProblem}
         ></textarea>
         <button
           onClick={handlePostProblem}
           className={`w-full mt-4 py-3 px-6 rounded-lg text-white font-semibold shadow-md transition duration-300 ease-in-out
             ${isPostingProblem ? 'bg-purple-400 cursor-not-allowed' : 'bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2'}`}
           disabled={isPostingProblem}
         >
           {isPostingProblem ? 'Posting Problem...' : 'Post Problem Anonymously'}
         </button>
         {aiCheckMessage && (
           <p className={`mt-3 text-center text-sm ${aiCheckMessage.includes('successfully') ? 'text-green-600' : 'text-red-600'}`}>
             {aiCheckMessage}
           </p>
         )}
       </div>


       {/* Section for AI-only advice */}
       <div className="mb-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
         <h2 className="text-xl font-bold text-blue-800 mb-4">Ask AI for Private Advice</h2>
         <p className="text-gray-700 text-sm mb-3">
           Not comfortable sharing publicly? Describe your problem here, and our AI will provide a kind suggestion just for you. This will not be posted.
         </p>
         <textarea
           className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200 ease-in-out resize-y min-h-[100px]"
           placeholder="Describe your problem privately to the AI..."
           value={privateProblemText}
           onChange={(e) => setPrivateProblemText(e.target.value)}
           rows="4"
           disabled={isGeneratingAdvice}
         ></textarea>
         <button
           onClick={handleAskAIForPrivateAdvice}
           className={`w-full mt-4 py-3 px-6 rounded-lg text-white font-semibold shadow-md transition duration-300 ease-in-out
             ${isGeneratingAdvice ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'}`}
           disabled={isGeneratingAdvice}
         >
           {isGeneratingAdvice ? 'Getting Advice...' : 'Get Private Advice from AI'}
         </button>
         {privateAdviceMessage && (
           <p className={`mt-3 text-center text-sm ${aiGeneratedAdvice ? 'text-green-600' : 'text-red-600'}`}>
             {privateAdviceMessage}
           </p>
         )}
         {aiGeneratedAdvice && (
           <div className="mt-4 p-4 bg-blue-100 rounded-lg border border-blue-300">
             <h3 className="text-md font-bold text-blue-800 mb-2">AI's Suggestion:</h3>
             <p className="text-gray-800 whitespace-pre-wrap">{aiGeneratedAdvice}</p>
           </div>
         )}
       </div>


       <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b-2 pb-2 border-purple-200">
         Community Problems & Suggestions
       </h2>
       <p className="text-sm text-gray-500 mb-4">Your User ID: <span className="font-mono text-xs bg-gray-200 px-2 py-1 rounded-md break-all">{userId}</span></p>


       {problems.length === 0 ? (
         <p className="text-center text-gray-500">No problems posted yet. Be the first to share!</p>
       ) : (
         <div className="space-y-6">
           {problems.map((problem) => (
             <ProblemItem
               key={problem.id}
               problem={problem}
               db={db}
               userId={userId}
               aiCheckFunction={aiCheckFunction}
               updateKindnessCounter={updateKindnessCounter} // Pass the update function
             />
           ))}
         </div>
       )}
     </div>
   </div>
 );
}


export default App;


