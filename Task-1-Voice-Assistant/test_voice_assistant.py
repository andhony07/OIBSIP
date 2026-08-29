"""
Unit test suite for Phase 1 & Phase 2 Voice Assistant logic.
Separates testable logic from hardware and live network dependencies.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import voice_assistant


class TestVoiceAssistantPhase1Regression(unittest.TestCase):

    def setUp(self):
        self.speak_patcher = patch("voice_assistant.speak")
        self.mock_speak = self.speak_patcher.start()

    def tearDown(self):
        self.speak_patcher.stop()

    def test_get_current_time(self):
        result = voice_assistant.get_current_time()
        self.assertTrue(result.startswith("The current time is "))
        self.assertTrue("AM" in result or "PM" in result)

    def test_get_current_date(self):
        result = voice_assistant.get_current_date()
        self.assertTrue(result.startswith("Today's date is "))
        self.assertIn("2026", result)

    @patch("webbrowser.open")
    def test_web_search(self, mock_browser_open):
        result = voice_assistant.web_search("Python tutorials")
        self.assertIn("python tutorials", result.lower())
        mock_browser_open.assert_called_once()

    def test_handle_command_greetings(self):
        res = voice_assistant.handle_command("Hello", custom_commands={})
        self.assertTrue(res)
        self.mock_speak.assert_called_with("Hello! How can I help you?")

    def test_handle_command_time(self):
        res = voice_assistant.handle_command("what time is it?", custom_commands={})
        self.assertTrue(res)
        spoken_arg = self.mock_speak.call_args[0][0]
        self.assertTrue(spoken_arg.startswith("The current time is "))

    def test_handle_command_date(self):
        res = voice_assistant.handle_command("What is today's date?", custom_commands={})
        self.assertTrue(res)
        spoken_arg = self.mock_speak.call_args[0][0]
        self.assertTrue(spoken_arg.startswith("Today's date is "))

    def test_handle_command_unknown(self):
        res = voice_assistant.handle_command("abracadabra 12345", custom_commands={})
        self.assertTrue(res)
        self.mock_speak.assert_called_with("Sorry, I didn't understand that command. Please try again.")

    def test_handle_command_exit(self):
        res = voice_assistant.handle_command("exit", custom_commands={})
        self.assertFalse(res)
        self.mock_speak.assert_called_with("Goodbye! Have a great day.")


class TestVoiceAssistantPhase2Advanced(unittest.TestCase):

    def setUp(self):
        self.speak_patcher = patch("voice_assistant.speak")
        self.mock_speak = self.speak_patcher.start()

    def tearDown(self):
        self.speak_patcher.stop()

    def test_nlu_intent_parsing(self):
        intent, params = voice_assistant.parse_intent("Could you tell me what the weather is like in Chennai?", {})
        self.assertEqual(intent, "weather")
        self.assertEqual(params.get("city"), "chennai")

        intent, params = voice_assistant.parse_intent("What time do we have right now?", {})
        self.assertEqual(intent, "time")

        intent, params = voice_assistant.parse_intent("Please search the internet for Python tutorials", {})
        self.assertEqual(intent, "web_search")
        self.assertIn("python tutorials", params.get("topic").lower())

        intent, params = voice_assistant.parse_intent("Remind me in 5 minutes to check my assignment", {})
        self.assertEqual(intent, "reminder")

        intent, params = voice_assistant.parse_intent("I need to send an email.", {})
        self.assertEqual(intent, "email")

        intent, params = voice_assistant.parse_intent("What is Python?", {})
        self.assertEqual(intent, "general_knowledge")

    def test_reminder_args_parsing(self):
        parsed = voice_assistant.parse_reminder_args("remind me in 5 minutes to submit my assignment")
        self.assertIsNotNone(parsed)
        duration, unit, message = parsed
        self.assertEqual(duration, 5)
        self.assertEqual(unit, "minutes")
        self.assertEqual(message, "submit my assignment")

        parsed = voice_assistant.parse_reminder_args("remind me in 10 seconds to test")
        self.assertIsNotNone(parsed)
        duration, unit, message = parsed
        self.assertEqual(duration, 10)
        self.assertEqual(unit, "seconds")
        self.assertEqual(message, "test")

    def test_schedule_reminder_validation(self):
        msg = voice_assistant.schedule_reminder("remind me in 0 seconds to do nothing")
        self.assertIn("must be a positive number", msg)

        msg = voice_assistant.schedule_reminder("remind me in 5 seconds to test reminder")
        self.assertIn("Reminder set for 5 second", msg)

    @patch.dict(os.environ, {}, clear=True)
    def test_weather_missing_key(self):
        msg = voice_assistant.get_weather("Chennai")
        self.assertIn("Weather API key is not configured", msg)

    @patch("requests.get")
    @patch.dict(os.environ, {"WEATHER_API_KEY": "dummy_test_key"})
    def test_weather_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Chennai",
            "main": {"temp": 31.4},
            "weather": [{"description": "clear sky"}]
        }
        mock_requests_get.return_value = mock_response

        msg = voice_assistant.get_weather("Chennai")
        self.assertIn("temperature in Chennai is 31 degrees Celsius with clear sky", msg)

    @patch.dict(os.environ, {}, clear=True)
    def test_email_missing_credentials(self):
        configured, msg = voice_assistant.check_email_credentials()
        self.assertFalse(configured)
        self.assertIn("Email configuration is incomplete", msg)

        voice_assistant.send_email_flow()
        self.mock_speak.assert_called_with("Email configuration is incomplete. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your environment or .env file.")

    def test_custom_commands_loading(self):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            json.dump({"open test": "https://example.com", "unsafe cmd": "calc.exe"}, f)
            temp_name = f.name

        try:
            cmds = voice_assistant.load_custom_commands(temp_name)
            self.assertIn("open test", cmds)
            self.assertEqual(cmds["open test"], "https://example.com")
            # Verify unsafe commands without http/https are filtered out
            self.assertNotIn("unsafe cmd", cmds)
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)

    def test_custom_commands_missing_or_malformed(self):
        cmds = voice_assistant.load_custom_commands("non_existent_file.json")
        self.assertEqual(cmds, {})

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write("{ malformed json }")
            temp_name = f.name

        try:
            cmds = voice_assistant.load_custom_commands(temp_name)
            self.assertEqual(cmds, {})
        finally:
            if os.path.exists(temp_name):
                os.remove(temp_name)

    def test_general_knowledge_answers(self):
        ans1 = voice_assistant.answer_question("Who created Python?")
        self.assertIn("Guido van Rossum", ans1)

        ans2 = voice_assistant.answer_question("What is Python?")
        self.assertIn("programming language", ans2)

        ans3 = voice_assistant.answer_question("What is the capital of France?")
        self.assertIn("Paris", ans3)


if __name__ == "__main__":
    unittest.main()
