require 'test_helper'

class LeaderBoardsControllerTest < ActionDispatch::IntegrationTest
  test "should get showAll" do
    get leader_boards_showAll_url
    assert_response :success
  end

  test "should get showGenreWise" do
    get leader_boards_showGenreWise_url
    assert_response :success
  end

  test "should get showTopicWise" do
    get leader_boards_showTopicWise_url
    assert_response :success
  end

end
