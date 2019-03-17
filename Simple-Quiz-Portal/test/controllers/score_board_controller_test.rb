require 'test_helper'

class ScoreBoardControllerTest < ActionDispatch::IntegrationTest
  test "should get show" do
    get score_board_show_url
    assert_response :success
  end

end
