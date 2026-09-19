import { useState } from "react";
import { useForm } from "react-hook-form";

import { generateBusinessPlan } from "../api/client";

export default function BusinessPlanForm() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const { register, handleSubmit, formState } = useForm({
    defaultValues: {
      project_name: "",
      industry: "",
      description: "",
      location: "",
      requested_investment: "",
    },
  });

  async function onSubmit(values) {
    setError("");
    setResult(null);

    try {
      const response = await generateBusinessPlan({
        project_data: {
          project_name: values.project_name,
          industry: values.industry,
          description: values.description,
          location: values.location,
          requested_investment: Number(values.requested_investment),
        },
      });
      setResult(response.data);
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Biznes-reja yaratib bo'lmadi.",
      );
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>
        Loyiha nomi
        <input {...register("project_name", { required: true })} />
      </label>
      <label>
        Sanoat
        <input {...register("industry", { required: true })} />
      </label>
      <label>
        Tavsif
        <textarea {...register("description", { required: true })} />
      </label>
      <label>
        Joylashuv
        <input {...register("location", { required: true })} />
      </label>
      <label>
        Kerakli investitsiya
        <input
          type="number"
          min="0.01"
          step="0.01"
          {...register("requested_investment", {
            required: true,
            min: 0.01,
          })}
        />
      </label>
      <button type="submit" disabled={formState.isSubmitting}>
        {formState.isSubmitting ? "Yaratilmoqda..." : "Biznes-reja yaratish"}
      </button>
      {error && <p role="alert">{error}</p>}
      {result && (
        <section aria-live="polite">
          <h2>Executive Summary</h2>
          <p>{result.executive_summary}</p>
          <h2>SWOT</h2>
          <p>{result.swot}</p>
          <h2>Marketing Plan</h2>
          <p>{result.marketing_plan}</p>
          <h2>Financial Plan</h2>
          <p>{result.financial_plan}</p>
        </section>
      )}
    </form>
  );
}
