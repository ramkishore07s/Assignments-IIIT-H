module QuizControllerHelper
  def is_admin?
    !!Admin.exists?(integer: current_user)
  end
end
