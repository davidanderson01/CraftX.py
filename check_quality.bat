@echo off
echo.
echo ====================================================
echo    CraftX.py Code Quality Report
echo    Generated: %date% %time%
echo ====================================================
echo.

echo 📊 OVERALL PROJECT SCORE:
echo ----------------------------
pylint scripts\migrate_storage.py craftxpy\memory\storage.py craftxpy\plugins\tools\large_storage_manager.py craftxpy\plugins\tools\file_hydration.py examples\large_storage_demo.py examples\storage_demo.py --score=yes --output-format=text | findstr "Your code has been rated"
echo.

echo 🚨 REMAINING ISSUES BY FILE:
echo -----------------------------

echo.
echo 📄 scripts\migrate_storage.py:
pylint scripts\migrate_storage.py --output-format=text | findstr /R "scripts.*:.*:"

echo.
echo 📄 craftxpy\memory\storage.py:
pylint craftxpy\memory\storage.py --output-format=text | findstr /R "storage.*:.*:"

echo.
echo 📄 craftxpy\plugins\tools\large_storage_manager.py:
pylint craftxpy\plugins\tools\large_storage_manager.py --output-format=text | findstr /R "large_storage_manager.*:.*:"

echo.
echo 📄 craftxpy\plugins\tools\file_hydration.py:
pylint craftxpy\plugins\tools\file_hydration.py --output-format=text | findstr /R "file_hydration.*:.*:"

echo.
echo 📄 examples\large_storage_demo.py:
pylint examples\large_storage_demo.py --output-format=text | findstr /R "large_storage_demo.*:.*:"

echo.
echo 📄 examples\storage_demo.py:
pylint examples\storage_demo.py --output-format=text | findstr /R "storage_demo.*:.*:"

echo.
echo ====================================================
echo    Report Complete
echo ====================================================
