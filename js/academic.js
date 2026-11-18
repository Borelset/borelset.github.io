(() => {
  "use strict";
  const tools = document.getElementById("publication-tools");
  if (tools) {
    const search = document.getElementById("publication-search");
    const year = document.getElementById("publication-year");
    const list = document.getElementById("publication-list");
    const groups = Array.from(list.querySelectorAll(".publication-year-group"));
    const topicButtons = Array.from(tools.querySelectorAll("[data-topic]"));
    const count = document.getElementById("publication-count");
    const empty = document.getElementById("publication-empty");
    const resetButton = document.getElementById("reset-filters");
    let activeTopic = "all";
    const filter = () => {
      const words = search.value
        .trim()
        .toLocaleLowerCase()
        .split(/\s+/)
        .filter(Boolean);
      let total = 0;
      groups.forEach((group) => {
        const matchesYear =
          year.value === "all" || group.dataset.year === year.value;
        let visible = 0;
        group.querySelectorAll(".paper").forEach((paper) => {
          const matchesTopic =
            activeTopic === "all" ||
            paper.dataset.topics.split(" ").includes(activeTopic);
          const matches =
            matchesYear &&
            matchesTopic &&
            words.every((word) => paper.dataset.search.includes(word));
          paper.hidden = !matches;
          if (matches) visible++;
        });
        group.hidden = visible === 0;
        total += visible;
      });
      topicButtons.forEach((button) =>
        button.setAttribute(
          "aria-pressed",
          String(button.dataset.topic === activeTopic),
        ),
      );
      count.textContent = `${total} publication${total === 1 ? "" : "s"}`;
      empty.hidden = total !== 0;
      resetButton.hidden =
        activeTopic === "all" && year.value === "all" && words.length === 0;
    };
    const reset = () => {
      search.value = "";
      year.value = "all";
      activeTopic = "all";
      filter();
    };
    topicButtons.forEach((button) =>
      button.addEventListener("click", () => {
        activeTopic = button.dataset.topic;
        filter();
      }),
    );
    search.addEventListener("input", filter);
    year.addEventListener("change", filter);
    resetButton.addEventListener("click", () => {
      reset();
      search.focus();
    });
    list.querySelectorAll("[data-paper-topic]").forEach((tag) => {
      tag.disabled = false;
    });
    list.addEventListener("click", (event) => {
      const tag = event.target.closest("[data-paper-topic]");
      if (!tag) return;
      const button = topicButtons.find(
        (item) => item.dataset.topic === tag.dataset.paperTopic,
      );
      if (button) {
        button.click();
        button.focus({ preventScroll: true });
        tools.closest("section").scrollIntoView({ block: "start" });
      }
    });
    // A direct paper link should reveal its target when filters hide it.
    const revealHash = () => {
      let id;
      try {
        id = decodeURIComponent(location.hash.slice(1));
      } catch (_) {
        return;
      }
      const target = document.getElementById(id);
      if (target && target.matches(".paper[hidden]")) {
        reset();
        target.scrollIntoView({ block: "center" });
      }
    };
    tools.hidden = false;
    filter();
    revealHash();
    window.addEventListener("hashchange", revealHash);
    if (navigator.clipboard && window.isSecureContext) {
      document.querySelectorAll(".copy-bibtex").forEach((button) => {
        button.hidden = false;
        button.addEventListener("click", async () => {
          try {
            await navigator.clipboard.writeText(
              button.closest(".bibtex-body").querySelector("pre").textContent,
            );
            button.textContent = "Copied!";
          } catch (_) {
            button.textContent = "Select citation to copy";
          }
          window.setTimeout(() => {
            button.textContent = "Copy citation";
          }, 2200);
        });
      });
    }
  }
  if ("IntersectionObserver" in window) {
    const navLinks = Array.from(
      document.querySelectorAll('.main-nav a[href*="#"]'),
    );
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          navLinks.forEach((link) => {
            const active = link.hash === `#${entry.target.id}`;
            link.classList.toggle("nav-current", active);
            if (active) link.setAttribute("aria-current", "location");
            else link.removeAttribute("aria-current");
          });
        });
      },
      { rootMargin: "-15% 0px -65% 0px", threshold: 0 },
    );
    ["about", "research", "publications", "experience"].forEach((id) => {
      const section = document.getElementById(id);
      if (section) observer.observe(section);
    });
  }
})();
