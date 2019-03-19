require 'test_helper'

class QuizzesControllerTest < ActionDispatch::IntegrationTest
  test "should get showTopics" do
    get quizzes_showTopics_url
    assert_response :success
  end

  test "should get showQuestions" do
    get quizzes_showQuestions_url
    assert_response :success
  end

  test "should get updateScore" do
    get quizzes_updateScore_url
    assert_response :success
  end

end
