function ResetExclusion() {
document
  .getElementById("reset-exclusions")
  .addEventListener("click", function () {
    const exclusionBoxes = document.querySelectorAll(
      'input[name="included_objects"]',
    );

    exclusionBoxes.forEach((box) => {
      box.checked = true;
    });
  });
}