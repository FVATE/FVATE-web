
$(document).ready ->

  $btn = $ '.diamond-icon'
  $invitecodeform = $ '#invite-code-form'
  $invitecodecontainer = $ '.content-13'
  $rsvpcontainer = $ '.content-37'
  $rsvpform = $ '#rsvp-form'
  $input = $invitecodeform.find('input[type="text"]')

  invitecodes = [
    "unvael",
  ]

  $btn.bind 'click', (e)->
    console.info '$btn.click:', e


  # invite-code form
  # ---------------------------------------------------------------------------
  $('#invitecode').bind 'keydown, keyup', (e)->
    invitecode = $input.val()

    if not invitecode?.length
      $btn.removeClass 'synesthesia'
      return

    $btn = $invitecodeform.find 'button'

    if invitecode.toLowerCase() in invitecodes
      # console.info 'FUCK YES'
      $btn.addClass 'synesthesia'
    else
      $btn.removeClass 'synesthesia'


  $invitecodeform.bind 'submit', (e)->
    # console.info '$invitecodeform.submit: ', e
    e.preventDefault()
    $this = $ @

    # INVITE CODE VALIDATION
    # ----------------------
    invitecode = $input.val()
    # console.info 'invitecode:', invitecode

    # ERROR
    if not invitecode?.length
      # console.error 'fuck emptiness.'
      # TODO: SET ERROR STATE
      return false

    isvalid = invitecode.toLowerCase() in invitecodes
    # console.warn 'isvalid:', isvalid
    if not isvalid
      console.error 'invite code is not accepted:', invitecode
      # TODO: SET ERROR STATE
      return false

    # SUCCESS
    on_submit_valid_invitecode()


  on_submit_valid_invitecode = ->
    # hide the invite-code form
    $invitecodecontainer.slideUp 666

    # show the rsvp form
    $rsvpcontainer.slideDown 666

    # ensure scroll position is set to the bottom of the page
    ypos = $(document).height() - $('.content-37').height()
    $("html, body").animate({scrollTop: ypos}, 1000)
    $('#rsvp-name').focus()


  # rsvp form
  # ---------------------------------------------------------------------------
  $rsvpform.bind 'submit', (e)->
    # console.info '$rsvpform.submit: ', e
    e.preventDefault()
    on_submit_rsvp $(@)


  on_submit_rsvp = ($this)->
    $inputs = $rsvpform.find('input')
    # console.info '$inputs:', $inputs

    data = {}
    $inputs.each (i, input)->
      $input = $(input)
      data[$input.attr('name')] = $input.val()

    # DB calls
    # --------
    # LOG USER TO DATABASE, SEND CONFIRMATION EMAIL
    unvael_rsvp.create data

    # UI updates
    # ----------
    # hide the rsvp form
    $('.signup-form').slideUp()
    # show the confirmation message
    $('.signup-form-done.unconfirmed').removeClass('unconfirmed')



# api helpers
# -----------------------------------------------------------------------------

unvael_rsvp =
  create: (data)->
    json_api_client "/api/rsvp/create", data, false


# json-api client wrapper
# -----------------------------------------------------------------------------
json_api_client = (url, data, cross_domain)->
  $.ajax
    url: url
    data: data
    type: 'POST'
    dataType: 'application/json'
    crossDomain: cross_domain
