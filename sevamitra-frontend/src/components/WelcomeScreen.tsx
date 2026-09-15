export default function WelcomeScreen() {
  return (
    <div className="flex flex-col items-center px-4 py-12 text-center">
      <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-blue-100 text-4xl dark:bg-blue-950">
        🇮🇳
      </div>

      <h2 className="text-3xl font-bold text-slate-900 dark:text-white sm:text-4xl">
        How can SevaMitra help you?
      </h2>

      <p className="mt-3 max-w-xl text-slate-600 dark:text-slate-400">
        Ask about government schemes, certificates, documents, eligibility
        and application procedures.
      </p>
    </div>
  );
}
