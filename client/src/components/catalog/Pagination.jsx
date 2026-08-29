export function Pagination({ currentPage, totalPages, onPageChange }) {
  if (totalPages <= 1) return null;

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  const Button = ({ label, page, disabled = false, isActive = false }) => (
    <button
      className={`pagination__button${isActive ? " is-active" : ""}`}
      type="button"
      aria-label={isActive ? `Sayfa ${page}, mevcut sayfa` : `${label} sayfasına git`}
      aria-current={isActive ? "page" : undefined}
      disabled={disabled}
      onClick={() => onPageChange(page)}
    >
      {label}
    </button>
  );

  return (
    <nav className="pagination" id="pagination" aria-label="Sayfalama">
      <Button label="Önceki" page={currentPage - 1} disabled={currentPage === 1} />
      {pages.map((page) => (
        <Button
          key={page}
          label={String(page)}
          page={page}
          isActive={page === currentPage}
        />
      ))}
      <Button
        label="Sonraki"
        page={currentPage + 1}
        disabled={currentPage === totalPages}
      />
    </nav>
  );
}
