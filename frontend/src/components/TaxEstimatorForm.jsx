import { useState } from "react";
import { useForm } from "react-hook-form";

import { estimateTax } from "../api/client";

export default function TaxEstimatorForm() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const { register, handleSubmit, formState } = useForm({
    defaultValues: {
      annual_turnover: "",
      employee_count: "",
    },
  });

  async function onSubmit(values) {
    setError("");
    setResult(null);

    try {
      const response = await estimateTax({
        annual_turnover: Number(values.annual_turnover),
        employee_count: Number(values.employee_count),
      });
      setResult(response.data);
    } catch (requestError) {
      setError(
        requestError.response?.data?.detail ||
          "Soliq hisob-kitobini bajarib bo'lmadi.",
      );
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>
        Yillik aylanma
        <input
          type="number"
          min="0"
          step="0.01"
          {...register("annual_turnover", { required: true, min: 0 })}
        />
      </label>
      <label>
        Xodimlar soni
        <input
          type="number"
          min="0"
          step="1"
          {...register("employee_count", { required: true, min: 0 })}
        />
      </label>
      <button type="submit" disabled={formState.isSubmitting}>
        {formState.isSubmitting ? "Hisoblanmoqda..." : "Soliqni hisoblash"}
      </button>
      {error && <p role="alert">{error}</p>}
      {result && (
        <section aria-live="polite">
          <p>Tavsiya etilgan rejim: {result.recommended_tax_regime}</p>
          <p>Taxminiy soliq: {result.estimated_tax}</p>
        </section>
      )}
    </form>
  );
}
